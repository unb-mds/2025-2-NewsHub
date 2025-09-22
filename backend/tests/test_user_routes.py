
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
    assert data['success'] is True
    assert "Usuário registrado com sucesso" in data['message']

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
    assert "Campo obrigatório ausente" in error_data['error']
    assert "'email'" in error_data['error']

def test_register_with_invalid_email_format(client):
    invalid_data = valid_user_data.copy()
    invalid_data['email'] = "email-invalido" 
    
    response = client.post(
        '/users/register',
        data=json.dumps(invalid_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    error_data = response.get_json()
    assert "Erro de validação em 'email': Formato de email inválido." in error_data['error']

def test_register_with_weak_password(client):
    invalid_data = valid_user_data.copy()
    invalid_data['password'] = "123" 
    
    response = client.post(
        '/users/register',
        data=json.dumps(invalid_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    error_data = response.get_json()
    assert "A senha deve ter no mínimo 8 caracteres" in error_data['error']

def test_login_successfully(client):
    client.post('/users/register', data=json.dumps(valid_user_data), content_type='application/json')
    
    login_data = {
        "email": valid_user_data["email"],
        "password": valid_user_data["password"]
    }
    
    response = client.post(
        '/users/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert "Login bem-sucedido" in data['message']
    assert data['data']['email'] == valid_user_data['email']
    assert 'access_token_cookie' in response.headers.get('Set-Cookie')

def test_login_with_wrong_password(client):

    client.post('/users/register', data=json.dumps(valid_user_data), content_type='application/json')
    
    login_data = {
        "email": valid_user_data["email"],
        "password": "wrongpassword"
    }
    
    response = client.post(
        '/users/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    assert response.status_code == 401
    error_data = response.get_json()
    assert "Credenciais inválidas" in error_data['error']