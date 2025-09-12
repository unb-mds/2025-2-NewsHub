import json

valid_user_data = {
    "full_name": "Test User",
    "email": "test.user@example.com",
    "password": "StrongPassword123"
}

def test_register_user_successfully(client):
    response = client.post(
        '/users/register',
        data=json.dumps(valid_user_data),
        content_type='application/json'
    )
    assert response.status_code == 201

    data = response.get_json()
    assert data['email'] == valid_user_data['email']
    assert data['full_name'] == valid_user_data['full_name']
    assert 'id' in data
    assert 'password' not in data
    assert 'password_hash' not in data

def test_register_with_duplicate_email(client):
    client.post('/users/register', data=json.dumps(valid_user_data), content_type='application/json')
    response = client.post(
        '/users/register',
        data=json.dumps(valid_user_data),
        content_type='application/json'
    )
    assert response.status_code == 409

    error_data = response.get_json()
    assert "E-mail já cadastrado" in error_data['error']

def test_register_with_missing_required_field(client):
    incomplete_data = valid_user_data.copy()
    del incomplete_data['email']

    response = client.post(
        '/users/register',
        data=json.dumps(incomplete_data),
        content_type='application/json'
    )
    assert response.status_code == 400

    error_data = response.get_json()
    assert "Preencha os campos obrigatório" in error_data['error']
    assert "'email'" in error_data['error']

import json
import pytest

valid_user_data = {
    "full_name": "Test User",
    "email": "test.user@example.com",
    "password": "StrongPassword123"
}

def test_register_user_successfully(client):
    response = client.post(
        '/users/register',
        data=json.dumps(valid_user_data),
        content_type='application/json'
    )
    assert response.status_code == 201

    data = response.get_json()
    assert data['email'] == valid_user_data['email']
    assert data['full_name'] == valid_user_data['full_name']
    assert 'id' in data
    assert 'password' not in data
    assert 'password_hash' not in data

def test_register_with_duplicate_email(client):
    client.post('/users/register', data=json.dumps(valid_user_data), content_type='application/json')
    response = client.post(
        '/users/register',
        data=json.dumps(valid_user_data),
        content_type='application/json'
    )
    assert response.status_code == 409

    error_data = response.get_json()
    assert "E-mail já cadastrado" in error_data['error']

def test_register_with_missing_required_field(client):
    incomplete_data = valid_user_data.copy()
    del incomplete_data['email']

    response = client.post(
        '/users/register',
        data=json.dumps(incomplete_data),
        content_type='application/json'
    )
    assert response.status_code == 400

    error_data = response.get_json()
    assert "Preencha os campos obrigatório" in error_data['error']
    assert "'email'" in error_data['error']

def test_register_with_invalid_email_format(client):
    invalid_data = valid_user_data.copy()
    invalid_data['email'] = "email-invalido" 
    
    response = client.post(
        '/users/register',
        data=json.dumps(invalid_data),
        content_type='application/json'
    )
    
    assert response.status_code == 409 
    error_data = response.get_json()
    assert "Formato de e-mail inválido" in error_data['error']


def test_register_with_weak_password(client):
    invalid_data = valid_user_data.copy()
    invalid_data['password'] = "123" 
    
    response = client.post(
        '/users/register',
        data=json.dumps(invalid_data),
        content_type='application/json'
    )
    
    assert response.status_code == 409
    error_data = response.get_json()
    assert "A senha deve ter pelo menos 8 caracteres" in error_data['error']