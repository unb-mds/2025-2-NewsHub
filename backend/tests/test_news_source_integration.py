import pytest
from flask.testing import FlaskClient
from app.models.user import User
from app.models.news_source import NewsSource
from app.entities.user_news_sources_entity import UserNewsSourceEntity

def test_add_source_to_user_success(client: FlaskClient, db):
    user_model = User(full_name="Test User", email="sourceuser@example.com", password="Password123")
    source_model = NewsSource(name="New Source", url="http://newsource.com")
    
    user_entity = user_model.to_orm()
    source_entity = source_model.to_orm()
    db.session.add_all([user_entity, source_entity])
    db.session.commit()

    login_res = client.post("/users/login", json={"email": "sourceuser@example.com", "password": "Password123"})
    assert login_res.status_code == 200

    auth_client, headers = get_auth_client(client, {"email": "sourceuser@example.com", "password": "Password123"})

    add_source_res = auth_client.post(
        "/news_sources/attach", 
        json={"source_id": source_entity.id},
        headers=headers
    )
    assert add_source_res.status_code == 200
    assert add_source_res.json["success"] is True
    assert "Fonte associada com sucesso." in add_source_res.json["message"]

    association = db.session.query(UserNewsSourceEntity).filter_by(user_id=user_entity.id, source_id=source_entity.id).first()
    assert association is not None

def test_add_existing_source_to_user(client: FlaskClient, db):
    user_model = User(full_name="Another User", email="anotheruser@example.com", password="Password123")
    source_model = NewsSource(name="Existing Source", url="http://existingsource.com")

    user_entity = user_model.to_orm()
    source_entity = source_model.to_orm()
    db.session.add_all([user_entity, source_entity])
    db.session.commit()

    auth_client, headers = get_auth_client(client, {"email": "anotheruser@example.com", "password": "Password123"})

    add_source_res = auth_client.post(
        "/news_sources/attach", 
        json={"source_id": source_entity.id},
        headers=headers
    )
    assert add_source_res.status_code == 200
    assert add_source_res.json["success"] is True

def test_add_source_missing_fields(client: FlaskClient, db):
    user_model = User(full_name="Test User 3", email="user3@example.com", password="Password123")
    user_entity = user_model.to_orm()
    db.session.add(user_entity)
    db.session.commit()
    
    auth_client, headers = get_auth_client(client, {"email": "user3@example.com", "password": "Password123"})

    add_source_res = auth_client.post(
        "/news_sources/attach", 
        json={},
        headers=headers
    )
    assert add_source_res.status_code == 400
    assert "source_id é obrigatório." in add_source_res.json["error"]

def test_list_user_sources(client: FlaskClient, db):
    user_model = User(full_name="List User", email="listuser@example.com", password="Password123")
    source1_model = NewsSource(name="Source One", url="http://sourceone.com")
    source2_model = NewsSource(name="Source Two", url="http://sourcetwo.com")

    user_entity = user_model.to_orm()
    source1_entity = source1_model.to_orm()
    source2_entity = source2_model.to_orm()
    db.session.add_all([user_entity, source1_entity, source2_entity])
    db.session.commit()

    db.session.add(UserNewsSourceEntity(user_id=user_entity.id, source_id=source1_entity.id))
    db.session.add(UserNewsSourceEntity(user_id=user_entity.id, source_id=source2_entity.id))
    db.session.commit()

    auth_client, _ = get_auth_client(client, {"email": "listuser@example.com", "password": "Password123"})

    list_res = auth_client.get("/news_sources/list_all_attached_sources")
    assert list_res.status_code == 200
    data = list_res.json["data"]
    assert len(data) == 2
    assert {item['name'] for item in data} == {"Source One", "Source Two"}

def test_remove_source_from_user(client: FlaskClient, db):
    user_model = User(full_name="Remove User", email="removeuser@example.com", password="Password123")
    source_model = NewsSource(name="Removable Source", url="http://removable.com")
    user_entity = user_model.to_orm()
    source_entity = source_model.to_orm()
    db.session.add_all([user_entity, source_entity])
    db.session.commit()
    db.session.add(UserNewsSourceEntity(user_id=user_entity.id, source_id=source_entity.id))
    db.session.commit()

    auth_client, headers = get_auth_client(client, {"email": "removeuser@example.com", "password": "Password123"})

    remove_res = auth_client.delete(f"/news_sources/detach/{source_entity.id}", headers=headers)
    assert remove_res.status_code == 200
    assert "Fonte desassociada com sucesso." in remove_res.json["message"]

def test_remove_non_existent_source(client: FlaskClient, db):
    user_model = User(full_name="Remove User 2", email="removeuser2@example.com", password="Password123")
    user_entity = user_model.to_orm()
    db.session.add(user_entity)
    db.session.commit()
    
    auth_client, headers = get_auth_client(client, {"email": "removeuser2@example.com", "password": "Password123"})

    remove_res = auth_client.delete("/news_sources/detach/999", headers=headers)
    assert remove_res.status_code == 404
    assert "Associação não encontrada para ser removida." in remove_res.json["error"]

def get_auth_client(client, user_data):
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }

    client.post(
        '/users/login',
        json=login_data,
    )
 
    csrf_cookie = client.get_cookie('csrf_access_token')
    csrf_token = ""
    if csrf_cookie:
        csrf_token = csrf_cookie.value
 
    headers = {'X-CSRF-TOKEN': csrf_token}
    return client, headers