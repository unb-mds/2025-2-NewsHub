import json
import pytest
from unittest.mock import patch, MagicMock
from app.controllers.user_controller import UserController
from app.models.exceptions import (
    UserValidationError,
    EmailInUseError,
    UserNotFoundError,
    InvalidPasswordError
)
from sqlalchemy.exc import IntegrityError
from flask import Flask
from flask_jwt_extended import JWTManager

class AttrDict(dict):
    """
    Uma classe de dicionário que também permite o acesso a chaves como atributos.
    """
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

@pytest.fixture(autouse=True)
def app_context():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super-secret-test-key"
    JWTManager(app)
    with app.test_request_context():
        yield

@pytest.fixture
def mock_service():
    with patch('app.controllers.user_controller.UserService') as MockUserService:
        yield MockUserService.return_value

@pytest.fixture
def user_controller(mock_service):
    controller = UserController()
    controller.service = mock_service
    return controller

# --- Testes de Registro ---

def test_register_key_error_returns_400(user_controller, mock_service):
    # Simulamos o serviço levantando o erro que o controller deve tratar
    mock_service.register.side_effect = KeyError("full_name")
    
    response, status_code = user_controller.register({})
    data = json.loads(response.data)

    assert status_code == 400
    
    # =====================================================================
    #  INÍCIO DA CORREÇÃO 1: Verificação robusta da mensagem de erro
    # =====================================================================
    assert "Campo obrigatório ausente" in data['error']
    assert "full_name" in data['error']
    # =====================================================================
    #  FIM DA CORREÇÃO 1
    # =====================================================================

def test_register_value_error_returns_400(user_controller, mock_service):
    mock_service.register.side_effect = ValueError("Formato de email inválido.")
    complete_data = {"full_name": "Test User", "email": "invalid", "password": "password123"}
    response, status_code = user_controller.register(complete_data)
    data = json.loads(response.data)
    assert status_code == 400
    assert "Formato de email inválido." in data['error']

def test_register_email_in_use_error_returns_409(user_controller, mock_service):
    mock_service.register.side_effect = EmailInUseError("E-mail já cadastrado")
    complete_data = {"full_name": "Test User", "email": "test@example.com", "password": "password123"}
    response, status_code = user_controller.register(complete_data)
    data = json.loads(response.data)
    assert status_code == 409
    assert "E-mail já cadastrado" in data['error']

@patch('app.controllers.user_controller.logging')
def test_register_unexpected_exception_returns_500(mock_logging, user_controller, mock_service):
    mock_service.register.side_effect = Exception("Database is down")
    complete_data = {"full_name": "Test User", "email": "test@example.com", "password": "password123"}
    response, status_code = user_controller.register(complete_data)
    data = json.loads(response.data)
    assert status_code == 500
    assert "Erro interno do servidor." in data['message']

# --- Testes de Login ---

@patch('app.controllers.user_controller.create_access_token', return_value="dummy_token")
@patch('app.controllers.user_controller.set_access_cookies')
def test_login_successfully(mock_set_cookies, mock_create_token, user_controller, mock_service):
    user_obj = AttrDict({"id": 1, "full_name": "Test User", "email": "test@example.com"})
    mock_service.login.return_value = user_obj

    response, status_code = user_controller.login({"email": "test@example.com", "password": "password"})
    data = json.loads(response.data)

    assert status_code == 200
    assert data['success'] is True
    
    response_user_data = data['data']
    assert response_user_data['full_name'] == user_obj.full_name
    assert response_user_data['email'] == user_obj.email
    
    mock_create_token.assert_called_once_with(identity='1')
    mock_set_cookies.assert_called_once()

def test_login_invalid_credentials_returns_401(user_controller, mock_service):
    mock_service.login.return_value = None
    response, status_code = user_controller.login({"email": "test@example.com", "password": "wrongpassword"})
    assert status_code == 401
    
def test_login_missing_fields_returns_400(user_controller, mock_service):
    mock_service.login.side_effect = KeyError("password")
    
    response, status_code = user_controller.login({"email": "test@example.com"})
    data = json.loads(response.data)
    
    assert status_code == 400
    
    # =====================================================================
    #  INÍCIO DA CORREÇÃO 2: Verificação robusta da mensagem de erro
    # =====================================================================
    assert "Dados de login inválidos ou ausentes" in data['error']
    assert "password" in data['error']
    # =====================================================================
    #  FIM DA CORREÇÃO 2
    # =====================================================================

# --- Demais Testes ---

@patch('app.controllers.user_controller.logging')
def test_login_unexpected_exception_returns_500(mock_logging, user_controller, mock_service):
    mock_service.login.side_effect = Exception("DB connection error")
    response, status_code = user_controller.login({"email": "test@example.com", "password": "password"})
    assert status_code == 500

def test_get_profile_user_not_found_returns_404(user_controller, mock_service):
    mock_service.get_profile.return_value = None
    response, status_code = user_controller.get_profile(user_id=999)
    assert status_code == 404

def test_update_profile_user_not_found_returns_404(user_controller, mock_service):
    mock_service.update_profile.side_effect = UserNotFoundError("Usuário não encontrado")
    response, status_code = user_controller.update_profile(user_id=999, data={})
    assert status_code == 404

def test_update_profile_email_in_use_returns_409(user_controller, mock_service):
    mock_service.update_profile.side_effect = EmailInUseError("O novo e-mail já está em uso.")
    response, status_code = user_controller.update_profile(user_id=1, data={})
    assert status_code == 409

def test_update_profile_validation_error_returns_400(user_controller, mock_service):
    mock_service.update_profile.side_effect = ValueError("Formato de email inválido.")
    response, status_code = user_controller.update_profile(user_id=1, data={})
    assert status_code == 400

def test_update_password_user_not_found_returns_404(user_controller, mock_service):
    mock_service.change_password.side_effect = UserNotFoundError("Usuário não encontrado.")
    response, status_code = user_controller.update_password(user_id=999, data={})
    assert status_code == 404

def test_update_password_validation_error_returns_400(user_controller, mock_service):
    mock_service.change_password.side_effect = ValueError("A senha deve ter no mínimo 8 caracteres.")
    response, status_code = user_controller.update_password(user_id=1, data={})
    assert status_code == 400