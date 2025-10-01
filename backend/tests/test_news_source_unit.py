import pytest
from unittest.mock import MagicMock
from app.services.news_source_service import NewsSourceService
from app.models.news_source import NewsSource
from app.models.exceptions import NewsSourceValidationError, NewsSourceNotFoundError, NewsSourceAlreadyAttachedError
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def mock_news_source_repository():
    return MagicMock()

@pytest.fixture
def mock_user_news_source_repository():
    return MagicMock()

@pytest.fixture
def news_source_service(mock_news_source_repository, mock_user_news_source_repository):
    return NewsSourceService(
        repo=mock_news_source_repository,
        user_source_repo=mock_user_news_source_repository
    )

def test_attach_source_to_user_success(news_source_service, mock_news_source_repository, mock_user_news_source_repository):
    user_id = 1
    source_id = 10
    mock_news_source_repository.find_by_id.return_value = NewsSource(id=source_id, name="Test", url="http://test.com")

    news_source_service.attach_source_to_user(user_id, source_id)

    mock_news_source_repository.find_by_id.assert_called_once_with(source_id)
    mock_user_news_source_repository.attach.assert_called_once_with(user_id, source_id)

def test_attach_source_to_user_source_not_found(news_source_service, mock_news_source_repository):
    user_id = 1
    source_id = 999
    mock_news_source_repository.find_by_id.return_value = None

    with pytest.raises(NewsSourceNotFoundError):
        news_source_service.attach_source_to_user(user_id, source_id)

def test_attach_source_to_user_integrity_error(news_source_service, mock_news_source_repository, mock_user_news_source_repository):
    user_id = 1
    source_id = 10
    mock_news_source_repository.find_by_id.return_value = NewsSource(id=source_id, name="Test", url="http://test.com")
    mock_user_news_source_repository.attach.side_effect = IntegrityError(None, None, None)

    with pytest.raises(IntegrityError):
        news_source_service.attach_source_to_user(user_id, source_id)

def test_attach_source_to_user_already_attached(news_source_service, mock_news_source_repository, mock_user_news_source_repository):
    user_id = 1
    source_id = 10
    mock_news_source_repository.find_by_id.return_value = NewsSource(id=source_id, name="Test", url="http://test.com")
    mock_user_news_source_repository.attach.side_effect = NewsSourceAlreadyAttachedError("Already attached")

    with pytest.raises(NewsSourceAlreadyAttachedError):
        news_source_service.attach_source_to_user(user_id, source_id)


def test_list_sources_by_user(news_source_service, mock_news_source_repository):
    user_id = 1
    sources = [NewsSource(id=1, name="A", url="http://a.com"), NewsSource(id=2, name="B", url="http://b.com")]
    mock_news_source_repository.list_by_user_id.return_value = sources

    result = news_source_service.list_by_user_id(user_id)
    
    assert len(result) == 2
    mock_news_source_repository.list_by_user_id.assert_called_once_with(user_id)

def test_list_all_sources(news_source_service, mock_news_source_repository):
    sources = [NewsSource(id=1, name="A", url="http://a.com"), NewsSource(id=2, name="B", url="http://b.com")]
    mock_news_source_repository.list_all.return_value = sources

    result = news_source_service.list_all()

    assert len(result) == 2
    mock_news_source_repository.list_all.assert_called_once()

def test_list_unassociated_by_user_id(news_source_service, mock_news_source_repository):
    user_id = 1
    sources = [NewsSource(id=3, name="C", url="http://c.com")]
    mock_news_source_repository.list_unassociated_by_user_id.return_value = sources

    result = news_source_service.list_unassociated_by_user_id(user_id)

    assert len(result) == 1
    assert result[0].name == "C"
    mock_news_source_repository.list_unassociated_by_user_id.assert_called_once_with(user_id)


def test_detach_source_from_user(news_source_service, mock_user_news_source_repository):
    user_id = 1
    source_id = 10

    news_source_service.detach_source_from_user(user_id, source_id)

    mock_user_news_source_repository.detach.assert_called_once_with(user_id, source_id)

def test_news_source_model_validation():
    with pytest.raises(NewsSourceValidationError, match="name: não pode ser vazio."):
        NewsSource(name="", url="http://valid.com")
    with pytest.raises(NewsSourceValidationError, match="url: não pode ser vazia."):
        NewsSource(name="Valid Name", url="")
    with pytest.raises(NewsSourceValidationError, match="url: formato inválido."):
        NewsSource(name="Valid Name", url="not-a-url")

def test_list_all_sources_exception(news_source_service, mock_news_source_repository):
    mock_news_source_repository.list_all.side_effect = Exception("DB Error")
    with pytest.raises(Exception, match="DB Error"):
        news_source_service.list_all()

def test_list_unassociated_by_user_id_exception(news_source_service, mock_news_source_repository):
    user_id = 1
    mock_news_source_repository.list_unassociated_by_user_id.side_effect = Exception("DB Error")
    with pytest.raises(Exception, match="DB Error"):
        news_source_service.list_unassociated_by_user_id(user_id)

def test_list_by_user_id_exception(news_source_service, mock_news_source_repository):
    user_id = 1
    mock_news_source_repository.list_by_user_id.side_effect = Exception("DB Error")
    with pytest.raises(Exception, match="DB Error"):
        news_source_service.list_by_user_id(user_id)