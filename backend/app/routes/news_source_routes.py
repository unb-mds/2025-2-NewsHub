from functools import wraps
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.news_source_controller import NewsSourceController

news_source_bp = Blueprint("news_sources", __name__)
news_sources_controller = NewsSourceController()

def get_user_id_from_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            user_id = int(get_jwt_identity())
            return f(user_id, *args, **kwargs)
        except (ValueError, TypeError):
            return jsonify({"success": False, "message": "Token inválido.", "data": None, "error": "Identidade inválida."}), 400
    return decorated

@news_source_bp.route("/list_all", methods=["GET"])
@jwt_required()
def list_all():
    return news_sources_controller.list_all()

@news_source_bp.route("/list_all_unattached_sources", methods=["GET"])
@jwt_required()
@get_user_id_from_token
def list_all_unattached_news_sources(user_id: int):
    return news_sources_controller.list_all_unattached_news_sources(user_id)

@news_source_bp.route("/list_all_attached_sources", methods=["GET"])
@jwt_required()
@get_user_id_from_token
def list_all_attached_sources(user_id: int):
    return news_sources_controller.list_all_attached_sources(user_id)

@news_source_bp.route("/attach", methods=["POST"])
@jwt_required()
@get_user_id_from_token
def attach_news_source(user_id: int):
    data = request.get_json() or {}
    return news_sources_controller.attach_news_source(user_id, data)

@news_source_bp.route("/detach/<int:news_source_id>", methods=["DELETE"])
@jwt_required()
@get_user_id_from_token
def detach_news_source(user_id: int, news_source_id: int):
    return news_sources_controller.detach_news_source(user_id, news_source_id)
