import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope='session')
def app():
    
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "super-secret-test-key",
        "WTF_CSRF_ENABLED": False,
        
    }

    _app = create_app(config_overrides=test_config)

    with _app.app_context():
        yield _app

@pytest.fixture(scope='function')
def db(app):
    _db.create_all()
    yield _db
    _db.session.remove()
    _db.drop_all()
        
@pytest.fixture(scope='function')
def client(app, db):
    return app.test_client()


