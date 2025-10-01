import pytest
from sqlalchemy.exc import IntegrityError
from app.repositories.topic_repository import TopicRepository
from app.models.topic import Topic
from app.entities.news_topic_entity import NewsTopicEntity

@pytest.fixture
def topic_repository(db):
    return TopicRepository(session=db.session)

def test_create_topic_sucessfully(topic_repository):
    topic_data = Topic(name="tecnologia")
    created_topic = topic_repository.create(topic_data)
    assert created_topic.id is not None
    assert created_topic.name == "tecnologia"
    
    
def test_create_topic_with_duplicate_casa_insensitivity(topic_repository):
    topic_data = Topic(name="TecNoLoGiA")
    created_topic = topic_repository.create(topic_data)
    
    assert created_topic.name == "tecnologia"
    
def test_create_duplicate_topic_fails(topic_repository):
    topic_repository.create(Topic(name="esportes"))
    
    with pytest.raises(IntegrityError):
        topic_repository.create(Topic(name="esportes"))
        
def test_find_by_name_sucessfully(topic_repository):
    topic_repository.create(Topic(name="ciencia"))
    
    found_topic = topic_repository.find_by_name("CiEnCiA")
    
    assert found_topic is not None
    assert found_topic.name == "ciencia"
    
    
def test_find_by_name_not_found(topic_repository):
    found_topic = topic_repository.find_by_name("nao-existe")
    
    assert found_topic is None
    