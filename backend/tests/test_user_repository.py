import pytest
from app.repositories.user_repository import UserRepository
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from datetime import date

@pytest.fixture
def user_repository(db):
    return UserRepository(session=db.session)

def test_create_user_successfully(user_repository):
    user_model = User(
        full_name="New User",
        email="new.user@example.com",
        password="ValidPassword123",
        birthdate=date(2000,1,1),
    )
    created_user = user_repository.create(user_model)
    assert created_user.id is not None
    assert created_user.email == user_model.email.lower()
    assert created_user.full_name == user_model.full_name

def test_create_user_with_duplicate_email_fails(user_repository):
    user_repository.create(User(full_name="user One", email="test@example.com", password="Password123"))
    
    with pytest.raises(IntegrityError):
        user_repository.create(User(full_name="User Two", email="test@example.com", password="Password456"))
        
        
def test_find_by_email_case_insensitive(user_repository):
    user_repository.create(User(full_name="Test User", email="test.user@example.com", password="Password123"))
    
    found_user = user_repository.find_by_email("TEST.USER@example.com")
    
    assert found_user is not None
    assert found_user.full_name == "Test User"
    

def test_find_by_id_successfully(user_repository):
    created_user = user_repository.create(User(full_name="Find Me", email="find.me@example.com", password="Password123"))
    
    found_user = user_repository.find_by_id(created_user.id)
    
    assert found_user is not None
    assert found_user.id == created_user.id
    
def test_update_user_successfully(user_repository):
    user = user_repository.create(User(full_name="Old Name", email="update.me@example.com", password="Password123"))
    
    user.full_name = "New Name"
    updated_user = user_repository.update(user)
    
    assert user.full_name == "New Name"
    assert updated_user.email == "update.me@example.com"
    