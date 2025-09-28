import pytest
from unittest.mock import MagicMock, call
from app.services.topic_service import TopicService
from app.models.topic import Topic, TopicValidationError
from sqlalchemy.exc import IntegrityError

@pytest.fixture
def mock_topic_repo():
    """Cria um mock para o repositório de tópicos."""
    return MagicMock()

@pytest.fixture
def mock_users_topics_repo():
    """Cria um mock para o repositório de associação entre usuários e tópicos."""
    return MagicMock()

@pytest.fixture
def topic_service(mock_topic_repo, mock_users_topics_repo):
    """Cria uma instância do TopicService com os repositórios mockados."""
    return TopicService(topic_repo=mock_topic_repo, users_topics_repo=mock_users_topics_repo)

def test_create_and_attach_new_topic(topic_service, mock_topic_repo, mock_users_topics_repo):
    user_id = 1
    data = {"name": "Test Topic"}
    original_name = data["name"]
    new_topic = Topic(id=1, name=original_name.lower().strip())
    
    mock_topic_repo.find_by_name.return_value = None
    mock_topic_repo.create.return_value = new_topic
    mock_users_topics_repo.attach.return_value = True
    
    result = topic_service.create_and_attach(user_id, data)
    
    assert result["topic"].name == new_topic.name
    assert result["attached"] is True
    mock_topic_repo.find_by_name.assert_called_once_with(original_name) 
    mock_users_topics_repo.attach.assert_called_once_with(user_id, new_topic.id)
    
def test_create_and_attach_existing_topic(topic_service, mock_topic_repo, mock_users_topics_repo):
    user_id = 1
    data = {"name": "Existing Topic"}
    original_name = data["name"]
    existing_topic = Topic(id=10, name=original_name.lower().strip())
    
    mock_topic_repo.find_by_name.return_value = existing_topic
    mock_users_topics_repo.attach.return_value = True
    
    result = topic_service.create_and_attach(user_id, data)
    
    assert result["topic"].name == existing_topic.name
    assert result["attached"] is True
    mock_topic_repo.find_by_name.assert_called_once_with(original_name) 
    mock_topic_repo.create.assert_not_called()
    mock_users_topics_repo.attach.assert_called_once_with(user_id, existing_topic.id)

def test_create_and_attach_existing_but_not_attached_topic(topic_service, mock_topic_repo, mock_users_topics_repo):
    user_id = 1
    data = {"name": "Existing Topic"}
    original_name = data["name"]
    existing_topic = Topic(id=10, name=original_name.lower().strip())
    
    mock_topic_repo.find_by_name.return_value = existing_topic
    mock_users_topics_repo.attach.return_value = False
    
    result = topic_service.create_and_attach(user_id, data)
    
    assert result["topic"].name == existing_topic.name
    assert result["attached"] is False
    mock_topic_repo.find_by_name.assert_called_once_with(original_name) 
    mock_topic_repo.create.assert_not_called()
    mock_users_topics_repo.attach.assert_called_once_with(user_id, existing_topic.id)
    
def test_find_by_user_returns_topics(topic_service, mock_topic_repo, mock_users_topics_repo):
    user_id = 1
    topic_ids = [1, 2, 3]
    topics = [
        Topic(id=1, name="topic 1"),
        Topic(id=2, name="topic 2"),
        Topic(id=3, name="topic 3"),
    ]
    
    mock_users_topics_repo.list_user_topic_ids.return_value = topic_ids
    
    # --- CORREÇÃO APLICADA AQUI ---
    # Mockamos o método 'find_by_id' que é chamado em loop.
    # 'side_effect' fará com que a cada chamada, um item da lista 'topics' seja retornado.
    mock_topic_repo.find_by_id.side_effect = topics
    
    result = topic_service.find_by_user(user_id)
    
    assert len(result) == 3
    assert [t.name for t in result] == ["topic 1", "topic 2", "topic 3"]
    mock_users_topics_repo.list_user_topic_ids.assert_called_once_with(user_id)
    
    # Verificamos se 'find_by_id' foi chamado para cada ID.
    expected_calls = [call(1), call(2), call(3)]
    mock_topic_repo.find_by_id.assert_has_calls(expected_calls)
    assert mock_topic_repo.find_by_id.call_count == 3


def test_detached_for_user_successful(topic_service, mock_users_topics_repo):
    user_id = 1
    topic_id = 10
    mock_users_topics_repo.detach.return_value = True
    
    result = topic_service.detach_for_user(user_id, topic_id)
    
    assert result is True
    mock_users_topics_repo.detach.assert_called_once_with(user_id, topic_id)
    
def test_detach_for_user_not_found(topic_service, mock_users_topics_repo):
    user_id = 1
    topic_id = 10
    mock_users_topics_repo.detach.return_value = False
    
    result = topic_service.detach_for_user(user_id, topic_id)
    
    assert result is False
    mock_users_topics_repo.detach.assert_called_once_with(user_id, topic_id)