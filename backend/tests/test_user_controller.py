import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_jwt_extended import JWTManager
from app.controllers.user_controller import UserController
from app.models.exceptions import (
    UserValidationError,
    UserNotFoundError,
    EmailInUseError,
    InvalidPasswordError
)

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

@pytest.fixture
def app_context():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super-secret-test-key"
    JWTManager(app)
    with app.app_context():
        yield

@pytest.fixture
def mock_service():
    with patch('app.controllers.user_controller.UserService') as mock:
        yield mock.return_value

@pytest.fixture
def controller(mock_service, app_context):
    controller = UserController()
    controller.service = mock_service
    return controller

def test_register_success(controller, mock_service):
    data = {"full_name": "Test User", "email": "test@example.com", "password": "password123"}

    mock_user = MagicMock()
    mock_user.to_dict.return_value = {"id": 1, "email": data["email"], "full_name": data["full_name"]}
    mock_service.register.return_value = mock_user 

    response, status_code = controller.register(data)
    json_data = response.get_json()

    assert status_code == 201
    assert json_data["success"] is True
    assert json_data["message"] == "Usuário registrado com sucesso."
    assert json_data["data"] is None
    assert json_data["error"] is None

def test_register_key_error_returns_400(controller, mock_service):
    mock_service.register.side_effect = KeyError("full_name")
    response, status_code = controller.register({})
    json_data = response.get_json()

    assert status_code == 400
    assert "Campo obrigatório ausente" in json_data["error"]

def test_register_value_error_returns_400(controller, mock_service):
    mock_service.register.side_effect = ValueError("Email inválido.")
    data = {"full_name": "Test", "email": "invalid", "password": "123"}
    response, status_code = controller.register(data)
    json_data = response.get_json()

    assert status_code == 400
    assert "Email inválido." in json_data["error"]

def test_register_email_in_use_error_returns_409(controller, mock_service):
    mock_service.register.side_effect = EmailInUseError("E-mail já cadastrado")
    data = {"full_name": "Test", "email": "test@example.com", "password": "123"}
    response, status_code = controller.register(data)
    json_data = response.get_json()

    assert status_code == 409
    assert "E-mail já cadastrado" in json_data["error"]

@patch('app.controllers.user_controller.logging')
def test_register_unexpected_exception_returns_500(mock_logging, controller, mock_service):
    mock_service.register.side_effect = Exception("Database is down")
    data = {"full_name": "Test", "email": "test@example.com", "password": "123"}
    response, status_code = controller.register(data)
    json_data = response.get_json()

    assert status_code == 500
    assert "Erro interno do servidor." in json_data["message"]

@patch('app.controllers.user_controller.create_access_token', return_value="dummy_token")
@patch('app.controllers.user_controller.set_access_cookies')
def test_login_successfully(mock_set_cookies, mock_create_token, controller, mock_service):
    user_obj = AttrDict({"id": 1, "full_name": "Test User", "email": "test@example.com"})
    mock_service.login.return_value = user_obj
    response, status_code = controller.login({"email": "test@example.com", "password": "password"})
    json_data = response.get_json()

    assert status_code == 200
    assert json_data["success"] is True
    mock_create_token.assert_called_once_with(identity='1')
    mock_set_cookies.assert_called_once()

def test_login_invalid_credentials_returns_401(controller, mock_service):
    mock_service.login.return_value = None
    response, status_code = controller.login({"email": "test@example.com", "password": "wrongpassword"})
    assert status_code == 401

def test_login_missing_fields_returns_400(controller, mock_service):
    mock_service.login.side_effect = KeyError("password")
    response, status_code = controller.login({"email": "test@example.com"})
    json_data = response.get_json()

    assert status_code == 400
    assert "Dados de login inválidos ou ausentes" in json_data["error"]

@patch('app.controllers.user_controller.logging')
def test_login_unexpected_exception_returns_500(mock_logging, controller, mock_service):
    mock_service.login.side_effect = Exception("DB connection error")
    response, status_code = controller.login({"email": "test@example.com", "password": "password"})
    assert status_code == 500

def test_get_profile_user_not_found_returns_404(controller, mock_service):
    mock_service.get_profile.return_value = None
    response, status_code = controller.get_profile(user_id=999)
    assert status_code == 404

def test_update_profile_user_not_found_returns_404(controller, mock_service):
    mock_service.update_profile.side_effect = UserNotFoundError("Usuário não encontrado")
    response, status_code = controller.update_profile(user_id=999, data={})
    assert status_code == 404

def test_update_profile_email_in_use_returns_409(controller, mock_service):
    mock_service.update_profile.side_effect = EmailInUseError("O novo e-mail já está em uso.")
    response, status_code = controller.update_profile(user_id=1, data={})
    assert status_code == 409

def test_update_profile_validation_error_returns_400(controller, mock_service):
    mock_service.update_profile.side_effect = ValueError("Formato de email inválido.")
    response, status_code = controller.update_profile(user_id=1, data={})
    assert status_code == 400

def test_update_password_user_not_found_returns_404(controller, mock_service):
    mock_service.change_password.side_effect = UserNotFoundError("Usuário não encontrado.")
    response, status_code = controller.update_password(user_id=999, data={})
    assert status_code == 404

def test_update_password_validation_error_returns_400(controller, mock_service):
    mock_service.change_password.side_effect = ValueError("A senha deve ter no mínimo 8 caracteres.")
    response, status_code = controller.update_password(user_id=1, data={})
    assert status_code == 400

@patch('app.controllers.user_controller.unset_jwt_cookies')
def test_logout_sucessfully(mock_unset_cookies, controller):
    user_id = 1
    response, status_code = controller.logout(user_id)
    json_data = response.get_json()

    assert status_code == 200
    assert json_data["success"] is True
    assert "Logout bem-sucedido" in json_data["message"]
    mock_unset_cookies.assert_called_once_with(response)
