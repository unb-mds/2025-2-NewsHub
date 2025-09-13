from flask import Blueprint, request
from app.controllers.user_controller import UserController

user_bp = Blueprint("users", __name__)

@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    return UserController.register(data)
