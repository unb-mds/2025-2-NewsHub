import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
from sqlalchemy.exc import IntegrityError
from backend.app.controllers.news_source_controller import NewsSourceController
from backend.app.models.news_source import NewsSource
from backend.app.models.exceptions import NewsSourceNotFoundError, NewsSourceAlreadyAttachedError, NewsSourceNotAttachedError

@pytest.fixture
def mock_service():
    with patch('backend.app.controllers.news_source_controller.NewsSourceService') as mock:
        yield mock.return_value

@pytest.fixture
def app_context():
    app = Flask(__name__)
    with app.app_context():
        yield

@pytest.fixture
def controller(mock_service, app_context):
    c = NewsSourceController()
    c.service = mock_service
    return c

def test_list_all_success(controller, mock_service):
    sources = [NewsSource(id=1, name="Test Source", url="http://test.com")]
    mock_service.list_all.return_value = sources
    response, status_code = controller.list_all()
    assert status_code == 200
    assert response.json["success"] is True
    assert len(response.json["data"]) == 1

def test_list_all_exception(controller, mock_service):
    mock_service.list_all.side_effect = Exception("DB Error")
    response, status_code = controller.list_all()
    assert status_code == 500
    assert response.json["success"] is False
    assert "Erro interno do servidor" in response.json["message"]

def test_list_all_unattached_success(controller, mock_service):
    user_id = 1
    sources = [NewsSource(id=2, name="Unattached", url="http://unattached.com")]
    mock_service.list_unassociated_by_user_id.return_value = sources
    response, status_code = controller.list_all_unattached_news_sources(user_id)
    assert status_code == 200
    assert response.json["success"] is True
    assert len(response.json["data"]) == 1

def test_list_all_unattached_exception(controller, mock_service):
    user_id = 1
    mock_service.list_unassociated_by_user_id.side_effect = Exception("DB Error")
    response, status_code = controller.list_all_unattached_news_sources(user_id)
    assert status_code == 500
    assert response.json["success"] is False

def test_list_all_attached_success(controller, mock_service):
    user_id = 1
    sources = [NewsSource(id=3, name="Attached", url="http://attached.com")]
    mock_service.list_by_user_id.return_value = sources
    response, status_code = controller.list_all_attached_sources(user_id)
    assert status_code == 200
    assert response.json["success"] is True
    assert len(response.json["data"]) == 1

def test_list_all_attached_exception(controller, mock_service):
    user_id = 1
    mock_service.list_by_user_id.side_effect = Exception("DB Error")
    response, status_code = controller.list_all_attached_sources(user_id)
    assert status_code == 500
    assert response.json["success"] is False

def test_attach_success(controller, mock_service):
    user_id = 1
    data = {"source_id": 10}
    mock_service.attach_source_to_user.return_value = None
    response, status_code = controller.attach_news_source(user_id, data)
    assert status_code == 200
    assert response.json["success"] is True
    mock_service.attach_source_to_user.assert_called_once_with(user_id, 10)

def test_attach_missing_source_id(controller):
    user_id = 1
    data = {}
    response, status_code = controller.attach_news_source(user_id, data)
    assert status_code == 400
    assert "source_id é obrigatório" in response.json["error"]

def test_attach_invalid_source_id(controller):
    user_id = 1
    data = {"source_id": "abc"}
    response, status_code = controller.attach_news_source(user_id, data)
    assert status_code == 400
    assert "deve ser um número inteiro válido" in response.json["error"]

def test_attach_source_not_found(controller, mock_service):
    user_id = 1
    data = {"source_id": 999}
    mock_service.attach_source_to_user.side_effect = NewsSourceNotFoundError("Not Found")
    response, status_code = controller.attach_news_source(user_id, data)
    assert status_code == 404
    assert "Not Found" in response.json["error"]

def test_attach_already_attached(controller, mock_service):
    user_id = 1
    data = {"source_id": 10}
    mock_service.attach_source_to_user.side_effect = NewsSourceAlreadyAttachedError("Conflict")
    response, status_code = controller.attach_news_source(user_id, data)
    assert status_code == 409
    assert "Conflict" in response.json["error"]

def test_attach_integrity_error(controller, mock_service):
    user_id = 1
    data = {"source_id": 10}
    mock_service.attach_source_to_user.side_effect = IntegrityError(None, None, None)
    response, status_code = controller.attach_news_source(user_id, data)
    assert status_code == 400
    assert "Falha de integridade" in response.json["message"]

def test_attach_generic_exception(controller, mock_service):
    user_id = 1
    data = {"source_id": 10}
    mock_service.attach_source_to_user.side_effect = Exception("Generic Error")
    response, status_code = controller.attach_news_source(user_id, data)
    assert status_code == 500
    assert "Erro interno do servidor" in response.json["message"]

def test_detach_success(controller, mock_service):
    user_id = 1
    source_id = 10
    mock_service.detach_source_from_user.return_value = None
    response, status_code = controller.detach_news_source(user_id, source_id)
    assert status_code == 200
    assert response.json["success"] is True
    mock_service.detach_source_from_user.assert_called_once_with(user_id, source_id)

def test_detach_not_attached(controller, mock_service):
    user_id = 1
    source_id = 999
    mock_service.detach_source_from_user.side_effect = NewsSourceNotAttachedError("Not Found")
    response, status_code = controller.detach_news_source(user_id, source_id)
    assert status_code == 404
    assert "Not Found" in response.json["error"]

def test_detach_generic_exception(controller, mock_service):
    user_id = 1
    source_id = 10
    mock_service.detach_source_from_user.side_effect = Exception("Generic Error")
    response, status_code = controller.detach_news_source(user_id, source_id)
    assert status_code == 500
    assert "Erro interno do servidor" in response.json["message"]