import json
import pytest
from unittest.mock import patch, MagicMock
from app.controllers.topic_controller import TopicController
from app.models.topic import Topic, TopicValidationError
from sqlalchemy.exc import IntegrityError
from flask import Flask

@pytest.fixture
def mock_service():
    with patch('app.controllers.topic_controller.TopicService') as mock:
        yield mock.return_value

@pytest.fixture
def app_context():
    app = Flask(__name__)
    with app.app_context():
        yield

def test_create_topic_validation_error_returns_400(topic_controller, mock_service):
    user_id = 1
    data = {}
    mock_service.create_and_attach.side_effect = TopicValidationError(
        "name", "não pode ser vazio."
    )

    response, status_code = topic_controller.create(user_id, data)

    assert status_code == 400
    assert response.json['success'] is False
    assert "Dados inválidos." in response.json['message']
    assert "name: não pode ser vazio." in response.json['error']
    mock_service.create_and_attach.assert_called_once_with(user_id, data)

def test_create_topic_integrity_error_returns_409(topic_controller, mock_service):
    user_id = 1
    data = {"name": "existing_topic"}
    mock_service.create_and_attach.side_effect = IntegrityError("Integrity Error", None, None)

    response, status_code = topic_controller.create(user_id, data)

    assert status_code == 409
    assert response.json['success'] is False
    assert "Erro de integridade." in response.json['message']
    assert "Conflito de dados." in response.json['error']
    mock_service.create_and_attach.assert_called_once_with(user_id, data)
    
@patch('app.controllers.topic_controller.logging')
def test_create_topic_unexpected_exception_returns_500(mock_logging, topic_controller, mock_service):
    user_id = 1
    data = {"name": "test"}
    mock_service.create_and_attach.side_effect = Exception("An unexpected error occurred.")
    
    response, status_code = topic_controller.create(user_id, data)
    
    assert status_code == 500
    assert response.json['success'] is False
    assert "Erro interno do servidor." in response.json['message']


def test_find_by_user_successful_returns_200(topic_controller, mock_service):
    user_id = 1
    topics = [
        Topic(id=1, name="topic1"),
        Topic(id=2, name="topic2")
    ]
    mock_service.find_by_user.return_value = topics
    
    response, status_code = topic_controller.find_by_user(user_id)
    
    assert status_code == 200
    assert response.json['success'] is True
    assert len(response.json['data']) == 2
    assert response.json['data'][0]['name'] == 'topic1'
    
@patch('app.controllers.topic_controller.logging')
def test_find_by_user_with_exception_returns_500(mock_logging, topic_controller, mock_service):
    user_id = 1
    mock_service.find_by_user.side_effect = Exception("DB error")
    
    response, status_code = topic_controller.find_by_user(user_id)
    
    assert status_code == 500
    assert response.json['success'] is False
    assert "Erro interno do servidor." in response.json['message']
    
def test_detach_my_topic_successful_returns_200(topic_controller, mock_service):
    user_id = 1
    topic_id = 1
    mock_service.detach_for_user.return_value = True
    
    response, status_code = topic_controller.detach_my_topic(user_id, topic_id)
    
    assert status_code == 200
    assert response.json['success'] is True
    assert "Tópico desvinculado com sucesso." in response.json['message']
    mock_service.detach_for_user.assert_called_once_with(user_id, topic_id)

def test_detach_my_topic_not_found_returns_404(topic_controller, mock_service):
    user_id = 1
    topic_id = 999
    mock_service.detach_for_user.return_value = False
    
    response, status_code = topic_controller.detach_my_topic(user_id, topic_id)
    
    assert status_code == 404
    assert response.json['success'] is False
    assert "Nada a remover." in response.json['error']
    mock_service.detach_for_user.assert_called_once_with(user_id, topic_id)

@patch('app.controllers.topic_controller.logging')
def test_detach_my_topic_with_exception_returns_500(mock_logging, topic_controller, mock_service):
    user_id = 1
    topic_id = 1
    mock_service.detach_for_user.side_effect = Exception("DB error")
    
    response, status_code = topic_controller.detach_my_topic(user_id, topic_id)
    
    assert status_code == 500
    assert response.json['success'] is False
    assert "Erro interno do servidor." in response.json['message']

@pytest.fixture
def topic_controller(mock_service, app_context):
    controller = TopicController()
    controller.service = mock_service
    return controller

def test_create_topic_validation_error_returns_400(topic_controller, mock_service):
    user_id = 1
    data = {}
    mock_service.create_and_attach.side_effect = TopicValidationError(
        "name", "não pode ser vazio."
    )

    response, status_code = topic_controller.create(user_id, data)

    assert status_code == 400
    assert response.json['success'] is False
    assert "Dados inválidos." in response.json['message']
    assert "name: não pode ser vazio." in response.json['error']
    mock_service.create_and_attach.assert_called_once_with(user_id, data)

def test_create_topic_integrity_error_returns_409(topic_controller, mock_service):
    user_id = 1
    data = {"name": "existing_topic"}
    mock_service.create_and_attach.side_effect = IntegrityError("Integrity Error", None, None)

    response, status_code = topic_controller.create(user_id, data)

    assert status_code == 409
    assert response.json['success'] is False
    assert "Erro de integridade." in response.json['message']
    assert "Conflito de dados." in response.json['error']
    mock_service.create_and_attach.assert_called_once_with(user_id, data)
    
@patch('app.controllers.topic_controller.logging')
def test_create_topic_unexpected_exception_returns_500(mock_logging, topic_controller, mock_service):
    user_id = 1
    data = {"name": "test"}
    mock_service.create_and_attach.side_effect = Exception("An unexpected error occurred.")
    
    response, status_code = topic_controller.create(user_id, data)
    
    assert status_code == 500
    assert response.json['success'] is False
    assert "Erro interno do servidor." in response.json['message']


def test_find_by_user_successful_returns_200(topic_controller, mock_service):
    user_id = 1
    topics = [
        Topic(id=1, name="topic1"),
        Topic(id=2, name="topic2")
    ]
    mock_service.find_by_user.return_value = topics
    
    response, status_code = topic_controller.find_by_user(user_id)
    
    assert status_code == 200
    assert response.json['success'] is True
    assert len(response.json['data']) == 2
    assert response.json['data'][0]['name'] == 'topic1'
    
@patch('app.controllers.topic_controller.logging')
def test_find_by_user_with_exception_returns_500(mock_logging, topic_controller, mock_service):
    user_id = 1
    mock_service.find_by_user.side_effect = Exception("DB error")
    
    response, status_code = topic_controller.find_by_user(user_id)
    
    assert status_code == 500
    assert response.json['success'] is False
    assert "Erro interno do servidor." in response.json['message']
    
def test_detach_my_topic_successful_returns_200(topic_controller, mock_service):
    user_id = 1
    topic_id = 1
    mock_service.detach_for_user.return_value = True
    
    response, status_code = topic_controller.detach_my_topic(user_id, topic_id)
    
    assert status_code == 200
    assert response.json['success'] is True
    assert "Tópico desvinculado com sucesso." in response.json['message']
    mock_service.detach_for_user.assert_called_once_with(user_id, topic_id)

def test_detach_my_topic_not_found_returns_404(topic_controller, mock_service):
    user_id = 1
    topic_id = 999
    mock_service.detach_for_user.return_value = False
    
    response, status_code = topic_controller.detach_my_topic(user_id, topic_id)
    
    assert status_code == 404
    assert response.json['success'] is False
    assert "Nada a remover." in response.json['error']
    mock_service.detach_for_user.assert_called_once_with(user_id, topic_id)

@patch('app.controllers.topic_controller.logging')
def test_detach_my_topic_with_exception_returns_500(mock_logging, topic_controller, mock_service):
    user_id = 1
    topic_id = 1
    mock_service.detach_for_user.side_effect = Exception("DB error")
    
    response, status_code = topic_controller.detach_my_topic(user_id, topic_id)
    
    assert status_code == 500
    assert response.json['success'] is False
    assert "Erro interno do servidor." in response.json['message']