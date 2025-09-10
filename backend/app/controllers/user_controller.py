from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from app.services.user_service import UserService

class UserController:
    @staticmethod
    def register():
        data = request.get_json()
        try:
            user = UserService.register(data)
            return jsonify({
                "id": user.id,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "email": user.email
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 409
        except IntegrityError:
            return jsonify({"error": "Erro de integridade no banco"}), 400
        except KeyError as e:
            return jsonify({"error": f"Campo obrigatório ausente: {e}"}), 400
