# backend/app/routes/topic_routes.py
from functools import wraps
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.topic_controller import TopicController

topic_bp = Blueprint("topics", __name__)
topic_controller = TopicController()

def get_user_id_from_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            user_id = int(get_jwt_identity())
            return f(user_id, *args, **kwargs)
        except (ValueError, TypeError):
            return jsonify({"success": False, "message": "Token inválido.", "data": None, "error": "Identidade inválida."}), 400
    return decorated

@topic_bp.post("/create")
@jwt_required()
@get_user_id_from_token
def create_topic(user_id: int):
    data = request.get_json() or {}
    return topic_controller.create(user_id, data)

@topic_bp.get("/list")
@jwt_required()
@get_user_id_from_token
def list_my_topics(user_id: int):
    return topic_controller.find_by_user(user_id)

@topic_bp.delete("/delete/<int:topic_id>")
@jwt_required()
@get_user_id_from_token
def detach_my_topic(user_id: int, topic_id: int):
    return topic_controller.detach_my_topic(user_id, topic_id)
