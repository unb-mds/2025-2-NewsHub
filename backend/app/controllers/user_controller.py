from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from app.services.user_service import UserService
from flask_jwt_extended import create_access_token, get_jwt_identity

user_service = UserService()

class UserController:
    @staticmethod
    def register(data):
        try:
            user = user_service.register(data)
            return jsonify({
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email
            }), 201
        except KeyError as e:
            return jsonify({"error": f"Preencha os campos obrigatório: {e}"}), 400
        except ValueError as e:
            return jsonify({"error": str(e)}), 409
        except IntegrityError:
            return jsonify({"error": "Erro de integridade no banco"}), 400
    @staticmethod
    def login():
        data = request.get_json()
        try:
            access_token = user_service.login(data)
            if access_token:
                return jsonify(access_token=access_token), 200
            else:         
                return jsonify({"error": "Credenciais inválidas"}), 401 
        except ValueError as e:
            return jsonify ({"error": str(e)}), 400
        
    @staticmethod
    def get_profile(user_id):
        user = user_service.get_profile(user_id)
        if user:
            return jsonify({
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "birthdate": user.birthdate.isoformat() if user.birthdate else None
            }), 200
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    @staticmethod
    def update_profile(user_id):
        current_user_id = get_jwt_identity()
        data = request.get_json()
        try:
            updated_user = user_service.update_profile(current_user_id, data)
            return jsonify({
                "id": updated_user.id,
                "full_name": updated_user.full_name,
                "email": updated_user.email
            }), 200
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        
    @staticmethod
    def update_password():
        current_user_id = get_jwt_identity
        data = request.get_json()
        try:
            user_service.change_password(current_user_id, data)
            return jsonify ({"message": "Senha alterada com sucesso"}), 200
        except ValueError as e: 
            return jsonify({"error": str(e)}), 400