from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
import logging
from app.services.topic_service import TopicService
from app.models.topic import TopicValidationError

class TopicController:
    def __init__(self):
        self.service = TopicService()

    def create(self, user_id: int, data: dict):
        try:
            result = self.service.create_and_attach(user_id, data)
            t = result["topic"]
            return jsonify({
                "success": True,
                "message": "Tópico criado com sucesso.",
                "data": {"id": t.id, "name": t.name, "state": t.state, "attached": result["attached"]},
                "error": None,
            }), 201
        except TopicValidationError as e:
            return jsonify({"success": False, "message": "Dados inválidos.", "data": None, "error": str(e)}), 400
        except IntegrityError:
            return jsonify({"success": False, "message": "Erro de integridade.", "data": None, "error": "Conflito de dados."}), 409
        except Exception as e:
            logging.error(f"Erro inesperado ao criar tópico: {e}", exc_info=True)
            return jsonify({"success": False, "message": "Erro interno do servidor.", "data": None, "error": "Ocorreu um erro inesperado."}), 500

    def find_by_user(self, user_id: int):
        try:
            items = self.service.find_by_user(user_id)
            data = [{"id": t.id, "name": t.name, "state": t.state} for t in items if t]
            return jsonify({"success": True, "message": "Tópicos recuperados com sucesso.", "data": data, "error": None}), 200
        except Exception as e:
            logging.error(f"Erro inesperado ao listar tópicos: {e}", exc_info=True)
            return jsonify({"success": False, "message": "Erro interno do servidor.", "data": None, "error": "Ocorreu um erro inesperado."}), 500

    def detach_my_topic(self, user_id: int, topic_id: int):
        try:
            response = self.service.detach_for_user(user_id, topic_id)
            if not response:
                return jsonify({"success": False, "message": "Relação não encontrada.", "data": None, "error": "Nada a remover."}), 404
            return jsonify({"success": True, "message": "Tópico desvinculado com sucesso.", "data": None, "error": None}), 200
        except Exception as e:
            logging.error(f"Erro inesperado ao desvincular tópico: {e}", exc_info=True)
            return jsonify({"success": False, "message": "Erro interno do servidor.", "data": None, "error": "Ocorreu um erro inesperado."}), 500
