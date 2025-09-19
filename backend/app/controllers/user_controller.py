from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from app.services.user_service import UserService
from flask_jwt_extended import create_access_token

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
