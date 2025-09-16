from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.user_controller import UserController

user_bp = Blueprint("users", __name__)

@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    return UserController.register(data)

@user_bp.route("/login", methods=["POST"])
def login():
    return UserController.login()


