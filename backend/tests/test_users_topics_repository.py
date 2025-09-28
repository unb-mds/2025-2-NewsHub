import pytest
from sqlalchemy.exc import SQLAlchemyError
from app.repositories.users_topics_repository import UsersTopicsRepository
from app.entities.user_topic_entity import UserTopicEntity
from unittest.mock import MagicMock, patch

@pytest.fixture
def users_topics_repository(db):
    return UsersTopicsRepository(session=db.session)

def test_attach_new_relation_successfully(users_topics_repository, db):
    user_id = 1
    topic_id = 1
    
    result = users_topics_repository.attach(user_id, topic_id)
    
    assert result is True
    relation = db.session.query(UserTopicEntity).filter_by(user_id=user_id, topic_id=topic_id).first()
    assert relation is not None

def test_attach_existing_relation_returns_false(users_topics_repository, db):
    user_id = 1
    topic_id = 1
    users_topics_repository.attach(user_id, topic_id)
    
    result = users_topics_repository.attach(user_id, topic_id)
    
    assert result is False

def test_attach_sqlalchemy_error_raises_exception(users_topics_repository, db):
    user_id = 1
    topic_id = 1
    
    with pytest.raises(SQLAlchemyError):
        with patch.object(db.session, 'commit', side_effect=SQLAlchemyError):
            users_topics_repository.attach(user_id, topic_id)
    
    with patch.object(db.session, 'rollback') as mock_rollback:
        with pytest.raises(SQLAlchemyError):
            with patch.object(db.session, 'commit', side_effect=SQLAlchemyError):
                users_topics_repository.attach(user_id, topic_id)
        mock_rollback.assert_called_once()
        
def test_detach_existing_relation_successfully(users_topics_repository, db):
    user_id = 1
    topic_id = 1
    users_topics_repository.attach(user_id, topic_id)
    
    result = users_topics_repository.detach(user_id, topic_id)
    
    assert result is True
    relation = db.session.query(UserTopicEntity).filter_by(user_id=user_id, topic_id=topic_id).first()
    assert relation is None

def test_detach_non_existing_relation_returns_false(users_topics_repository, db):
    user_id = 1
    topic_id = 999
    
    result = users_topics_repository.detach(user_id, topic_id)
    
    assert result is False

def test_detach_sqlalchemy_error_raises_exception(users_topics_repository, db):
    user_id = 1
    topic_id = 1
    users_topics_repository.attach(user_id, topic_id)
    
    with pytest.raises(SQLAlchemyError):
        with patch.object(db.session, 'commit', side_effect=SQLAlchemyError):
            users_topics_repository.detach(user_id, topic_id)
    
    with patch.object(db.session, 'rollback') as mock_rollback:
        with pytest.raises(SQLAlchemyError):
            with patch.object(db.session, 'commit', side_effect=SQLAlchemyError):
                users_topics_repository.detach(user_id, topic_id)
        mock_rollback.assert_called_once()

def test_list_user_topic_ids_returns_correct_ids(users_topics_repository, db):
    user_id = 1
    topic_ids = [10, 20, 30]
    
    for tid in topic_ids:
        db.session.add(UserTopicEntity(user_id=user_id, topic_id=tid))
    db.session.commit()
    
    result = users_topics_repository.list_user_topic_ids(user_id)
    
    assert sorted(result) == sorted(topic_ids)

def test_list_user_topic_ids_no_topics_returns_empty_list(users_topics_repository, db):
    user_id = 999
    result = users_topics_repository.list_user_topic_ids(user_id)
    
    assert result == []