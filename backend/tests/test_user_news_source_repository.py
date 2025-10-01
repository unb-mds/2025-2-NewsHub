import pytest
from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.repositories.user_news_source_repository import UserNewsSourceRepository
from app.models.exceptions import NewsSourceAlreadyAttachedError, NewsSourceNotAttachedError
from app.entities.user_news_sources_entity import UserNewsSourceEntity

@pytest.fixture
def user_news_source_repo(db):
    return UserNewsSourceRepository(session=db.session)

def test_attach_success(user_news_source_repo, db):
    user_id, source_id = 1, 1
    user_news_source_repo.attach(user_id, source_id)
    relation = db.session.query(UserNewsSourceEntity).filter_by(user_id=user_id, source_id=source_id).one()
    assert relation is not None

def test_attach_already_exists_raises_error(user_news_source_repo, db):
    user_id, source_id = 1, 1
    user_news_source_repo.attach(user_id, source_id)
    with pytest.raises(NewsSourceAlreadyAttachedError):
        user_news_source_repo.attach(user_id, source_id)

def test_attach_integrity_error(user_news_source_repo, db):
    with patch.object(db.session, 'commit', side_effect=IntegrityError(None, None, None)):
        with pytest.raises(IntegrityError):
            user_news_source_repo.attach(1, 999) # Assuming source 999 does not exist

def test_attach_sqlalchemy_error(user_news_source_repo, db):
    with patch.object(db.session, 'commit', side_effect=SQLAlchemyError("DB Error")):
        with pytest.raises(SQLAlchemyError):
            user_news_source_repo.attach(1, 1)

def test_detach_success(user_news_source_repo, db):
    user_id, source_id = 1, 1
    db.session.add(UserNewsSourceEntity(user_id=user_id, source_id=source_id))
    db.session.commit()

    user_news_source_repo.detach(user_id, source_id)

    relation = db.session.query(UserNewsSourceEntity).filter_by(user_id=user_id, source_id=source_id).first()
    assert relation is None

def test_detach_not_existing_raises_error(user_news_source_repo):
    with pytest.raises(NewsSourceNotAttachedError):
        user_news_source_repo.detach(1, 999)

def test_detach_sqlalchemy_error(user_news_source_repo, db):
    user_id, source_id = 1, 1
    db.session.add(UserNewsSourceEntity(user_id=user_id, source_id=source_id))
    db.session.commit()

    with patch.object(db.session, 'commit', side_effect=SQLAlchemyError("DB Error")):
        with pytest.raises(SQLAlchemyError):
            user_news_source_repo.detach(user_id, source_id)

def test_attach_logs_and_raises_on_integrity_error(user_news_source_repo):
    with patch('app.repositories.user_news_source_repository.logging') as mock_logging:
        with patch.object(user_news_source_repo.session, 'commit', side_effect=IntegrityError(None, None, None)):
            with pytest.raises(IntegrityError):
                user_news_source_repo.attach(1, 1)
            mock_logging.warning.assert_called_once()