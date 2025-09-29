import pytest
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from unittest.mock import patch
from backend.app.repositories.news_source_repository import NewsSourceRepository
from backend.app.models.news_source import NewsSource
from backend.app.entities.user_entity import UserEntity
from backend.app.entities.news_source_entity import NewsSourceEntity
from backend.app.entities.user_news_sources_entity import UserNewsSourceEntity

@pytest.fixture
def news_source_repo(db):
    return NewsSourceRepository(session=db.session)

def test_create_news_source_success(news_source_repo):
    source_model = NewsSource(name="Test Source", url="http://testsource.com")
    created_source = news_source_repo.create(source_model)
    assert created_source.id is not None
    assert created_source.name == "Test Source"

def test_create_duplicate_url_fails(news_source_repo):
    source1 = NewsSource(name="Source One", url="http://duplicate.com")
    news_source_repo.create(source1)
    source2 = NewsSource(name="Source Two", url="http://duplicate.com")
    with pytest.raises(IntegrityError):
        news_source_repo.create(source2)

def test_find_by_id(news_source_repo, db):
    source_entity = NewsSourceEntity(name="Find Me", url="http://findme.com")
    db.session.add(source_entity)
    db.session.commit()
    found = news_source_repo.find_by_id(source_entity.id)
    assert found is not None
    assert found.id == source_entity.id

def test_find_by_url(news_source_repo, db):
    source_entity = NewsSourceEntity(name="Find By URL", url="http://findbyurl.com")
    db.session.add(source_entity)
    db.session.commit()
    found = news_source_repo.find_by_url("http://findbyurl.com")
    assert found is not None
    assert found.url == "http://findbyurl.com"

def test_list_all(news_source_repo, db):
    db.session.add(NewsSourceEntity(name="A", url="http://a.com"))
    db.session.add(NewsSourceEntity(name="B", url="http://b.com"))
    db.session.commit()
    sources = news_source_repo.list_all()
    assert len(sources) == 2

def test_list_by_user_id(news_source_repo, db):
    user = UserEntity(email="user@test.com", _password_hash="hash")
    s1 = NewsSourceEntity(name="S1", url="http://s1.com")
    s2 = NewsSourceEntity(name="S2", url="http://s2.com")
    db.session.add_all([user, s1, s2])
    db.session.commit()
    db.session.add(UserNewsSourceEntity(user_id=user.id, source_id=s1.id))
    db.session.commit()
    
    user_sources = news_source_repo.list_by_user_id(user.id)
    assert len(user_sources) == 1
    assert user_sources[0].name == "S1"

def test_list_unassociated_by_user_id(news_source_repo, db):
    user = UserEntity(email="user2@test.com", _password_hash="hash")
    s1 = NewsSourceEntity(name="S1-un", url="http://s1un.com")
    s2 = NewsSourceEntity(name="S2-un", url="http://s2un.com") 
    s3 = NewsSourceEntity(name="S3-un", url="http://s3un.com") 
    db.session.add_all([user, s1, s2, s3])
    db.session.commit()
    db.session.add(UserNewsSourceEntity(user_id=user.id, source_id=s1.id))
    db.session.commit()

    unassociated = news_source_repo.list_unassociated_by_user_id(user.id)
    assert len(unassociated) == 2
    names = {s.name for s in unassociated}
    assert "S2-un" in names
    assert "S3-un" in names

def test_sqlalchemy_error_on_list(news_source_repo):
    with patch.object(news_source_repo.session, 'execute', side_effect=SQLAlchemyError("DB Error")):
        with pytest.raises(SQLAlchemyError):
            news_source_repo.list_all()