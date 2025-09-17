from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
import logging
from app.services.user_service import UserService
from flask_jwt_extended import set_access_cookies, create_access_token
from app.models.exceptions import UserNotFoundError, EmailInUseError

class UserController:
    def __init__(self):
        self.service = UserService()

    def register(self, data):
        try:
            self.service.register(data)
            return jsonify(
                {
                    "success": True,
                    "message": "Usuário registrado com sucesso.",
                    "data": None,
                    "error": None,
                }
            ), 201
        except KeyError as e:
            return jsonify(
                {
                    "success": False,
                    "message": "Dados inválidos.",
                    "data": None,
                    "error": f"Campo obrigatório ausente: {e}",
                }
            ), 400
        except ValueError as e:  # Captura erros de validação do modelo (nome, formato de senha, etc)
            return jsonify(
                {
                    "success": False,
                    "message": "Dados inválidos.",
                    "data": None,
                    "error": str(e),
                }
            ), 400
        except EmailInUseError as e: 
            return jsonify(
                {
                    "success": False,
                    "message": "Conflito de dados.",
                    "data": None,
                    "error": str(e),
                }
            ), 409
        except IntegrityError: 
            return jsonify(
                {
                    "success": False,
                    "message": "Erro de integridade.",
                    "data": None,
                    "error": "Ocorreu um erro de integridade no banco de dados. O e-mail pode já estar em uso.",
                }
            ), 409
        except Exception as e:
            logging.error(f"Erro inesperado ao registrar usuário: {e}", exc_info=True)
            return jsonify(
                {
                    "success": False,
                    "message": "Erro interno do servidor.",
                    "data": None,
                    "error": "Ocorreu um erro inesperado ao registrar o usuário.",
                }
            ), 500

    def login(self, data):
        try:
            user = self.service.login(data)
            if not user or not user.id:
                return jsonify(
                    {
                        "success": False,
                        "message": "Falha na autenticação.",
                        "data": None,
                        "error": "Credenciais inválidas.",
                    }
                ), 401

            access_token = create_access_token(identity=str(user.id))
            logging.info(f"Token de acesso criado para o usuário ID: {user.id}")

            response = jsonify(
                {
                    "success": True,
                    "message": "Login bem-sucedido.",
                    "data": None,
                    "error": None,
                }
            )
            set_access_cookies(response, access_token)
            return response, 200

        except (KeyError, ValueError) as e:
            return jsonify(
                {
                    "success": False,
                    "message": "Dados inválidos.",
                    "data": None,
                    "error": f"Dados de login inválidos ou ausentes: {e}",
                }
            ), 400
        except Exception as e:
            logging.error(f"Erro inesperado durante o login: {e}", exc_info=True)
            return jsonify(
                {
                    "success": False,
                    "message": "Erro interno do servidor.",
                    "data": None,
                    "error": "Ocorreu um erro inesperado durante o login.",
                }
            ), 500

    def get_profile(self, user_id):
        try:
            user = self.service.get_profile(user_id)
            if user:
                user_data = {
                    "full_name": user.full_name,
                    "email": user.email,
                    "birthdate": user.birthdate.isoformat() if user.birthdate else None,
                }
                return jsonify(
                    {
                        "success": True,
                        "message": "Perfil do usuário recuperado com sucesso.",
                        "data": user_data,
                        "error": None,
                    }
                ), 200
            return jsonify(
                {
                    "success": False,
                    "message": "Usuário não encontrado.",
                    "data": None,
                    "error": "O usuário solicitado não existe.",
                }
            ), 404
        except Exception as e:
            logging.error(f"Erro inesperado ao buscar perfil (ID: {user_id}): {e}", exc_info=True)
            return jsonify(
                {
                    "success": False,
                    "message": "Erro interno do servidor.",
                    "data": None,
                    "error": "Ocorreu um erro inesperado ao buscar o perfil.",
                }
            ), 500
    def update_profile(self, user_id, data):
        try:
            updated_user = self.service.update_profile(user_id, data)
            user_data = {
                "full_name": updated_user.full_name,
                "email": updated_user.email,
                "birthdate": updated_user.birthdate.isoformat()
                if updated_user.birthdate
                else None,
            }
            return jsonify(
                {
                    "success": True,
                    "message": "Perfil atualizado com sucesso.",
                    "data": user_data,
                    "error": None,
                }
            ), 200

        except UserNotFoundError as e:
            return jsonify(
                {
                    "success": False,
                    "message": "Usuário não encontrado.",
                    "data": None,
                    "error": str(e),
                }
            ), 404
        except EmailInUseError as e:
            return jsonify(
                {
                    "success": False,
                    "message": "Conflito de dados.",
                    "data": None,
                    "error": str(e),
                }
            ), 409
        except ValueError as e:
            return jsonify(
                {
                    "success": False,
                    "message": "Erro de validação.",
                    "data": None,
                    "error": str(e),
                }
            ), 400
        except Exception as e:
            logging.error(f"Erro inesperado ao atualizar perfil (ID: {user_id}): {e}", exc_info=True)
            return jsonify(
                {
                    "success": False,
                    "message": "Erro interno do servidor.",
                    "data": None,
                    "error": "Ocorreu um erro inesperado ao atualizar o perfil.",
                }
            ), 500

    def update_password(self, user_id, data):
        try:
            self.service.change_password(user_id, data)
            return jsonify(
                {
                    "success": True,
                    "message": "Senha alterada com sucesso.",
                    "data": None,
                    "error": None,
                }
            ), 200
        except UserNotFoundError as e:
            return jsonify(
                {
                    "success": False,
                    "message": "Usuário não encontrado.",
                    "data": None,
                    "error": str(e),
                }
            ), 404
        except ValueError as e:
            return jsonify(
                {
                    "success": False,
                    "message": "Erro de validação.",
                    "data": None,
                    "error": str(e),
                }
            ), 400
        except Exception as e:
            logging.error(f"Erro inesperado ao alterar senha (ID: {user_id}): {e}", exc_info=True)
            return jsonify(
                {
                    "success": False,
                    "message": "Erro interno do servidor.",
                    "data": None,
                    "error": "Ocorreu um erro inesperado ao alterar a senha.",
                }
            ), 500