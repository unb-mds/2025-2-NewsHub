
import logging
from flask import request, jsonify
from app.services.news_source_service import NewsSourceService
from app.models.exceptions import NewsSourceNotFoundError, NewsSourceAlreadyAttachedError, NewsSourceNotAttachedError
from sqlalchemy.exc import IntegrityError


class NewsSourceController:
    def __init__(self):
        self.service = NewsSourceService()

    def list_all(self):
        try:
            sources = self.service.list_all()
            sources_data = [{"id": s.id, "name": s.name, "url": s.url} for s in sources]
            return jsonify({
                "success": True,
                "message": "Fontes de notícias listadas com sucesso.",
                "data": sources_data,
                "error": None
            }), 200
        except Exception as e:
            logging.error(f"Erro ao listar fontes de notícias: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno do servidor.",
                "data": None,
                "error": "Ocorreu um erro inesperado ao listar as fontes de notícias."
            }), 500
        

    def list_all_unattached_news_sources(self, user_id: int):
        try:
            sources = self.service.list_unassociated_by_user_id(user_id)
            sources_data = [{"id": s.id, "name": s.name, "url": s.url} for s in sources]
            return jsonify({
                "success": True,
                "message": "Fontes de notícias não associadas listadas com sucesso.",
                "data": sources_data,
                "error": None
            }), 200
        except Exception as e:
            logging.error(f"Erro ao listar fontes não associadas: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno do servidor.",
                "data": None,
                "error": "Ocorreu um erro inesperado ao listar as fontes de notícias."
            }), 500

    def list_all_attached_sources(self, user_id: int):
        try:
            sources = self.service.list_by_user_id(user_id)
            sources_data = [{"id": s.id, "name": s.name, "url": s.url} for s in sources]
            return jsonify({
                "success": True,
                "message": "Fontes de notícias associadas listadas com sucesso.",
                "data": sources_data,
                "error": None
            }), 200
        except Exception as e:
            logging.error(f"Erro ao listar fontes associadas: {e}", exc_info=True)
            return jsonify({
                "success": False,
                "message": "Erro interno do servidor.",
                "data": None,
                "error": "Ocorreu um erro inesperado ao listar as fontes de notícias."
            }), 500

    def attach_news_source(self, user_id: int, data: dict):
        try:
            source_id_raw = data.get("source_id")
            if source_id_raw is None:
                return jsonify({
                    "success": False, 
                    "message": "Dados inválidos.", 
                    "data": None, 
                    "error": "source_id é obrigatório."
                }), 400
            source_id = int(source_id_raw)
            self.service.attach_source_to_user(user_id, source_id)
            return jsonify({
                "success": True, 
                "message": "Fonte associada com sucesso.", 
                "data": None, 
                "error": None
            }), 200
        except (ValueError, TypeError):
            return jsonify({
                "success": False,
                "message": "Dados inválidos.",
                "data": None,
                "error": "O campo 'source_id' deve ser um número inteiro válido."
            }), 400
        except NewsSourceNotFoundError as e:
            return jsonify({
                "success": False, 
                "message": "Recurso não encontrado.", 
                "data": None, 
                "error": str(e)
            }), 404
        except NewsSourceAlreadyAttachedError as e:
            return jsonify({
                "success": False, 
                "message": "Conflito.", 
                "data": None, 
                "error": str(e)
            }), 409
        except IntegrityError:
            # Este erro pode ocorrer se o user_id for inválido, por exemplo.
            return jsonify({
                "success": False, 
                "message": "Falha de integridade.", 
                "data": None, 
                "error": "Não foi possível associar a fonte. Verifique os IDs."
            }), 400
        except Exception as e:
            logging.error(f"Erro ao associar fonte: {e}", exc_info=True)
            return jsonify({
                "success": False, 
                "message": "Erro interno do servidor.", 
                "data": None, 
                "error": "Ocorreu um erro inesperado."
            }), 500

    def detach_news_source(self, user_id: int, news_source_id: int):
        try:
            self.service.detach_source_from_user(user_id, news_source_id)
            return jsonify({
                "success": True, 
                "message": "Fonte desassociada com sucesso.", 
                "data": None, 
                "error": None
            }), 200
        except NewsSourceNotAttachedError as e:
            return jsonify({
                "success": False, 
                "message": "Recurso não encontrado.", 
                "data": None, 
                "error": str(e)
            }), 404
        except Exception as e:
            logging.error(f"Erro ao desassociar fonte: {e}", exc_info=True)
            return jsonify({
                "success": False, 
                "message": "Erro interno do servidor.", 
                "data": None, 
                "error": "Ocorreu um erro inesperado." 
            }), 500
