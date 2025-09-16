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

@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    return UserController.get_profile()

@user_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    return UserController.update_profile()

@user_bp.route("/profile/password", methods=["PUT"])
@jwt_required
def update_my_password():
    return UserController.update_password()

