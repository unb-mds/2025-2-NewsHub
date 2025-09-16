import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.extensions import db
from app.routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)

    CORS(app)
    
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key-default")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init extensions
    db.init_app(app)
    jwt = JWTManager(app)

    from app.entities import user_entity 

    @app.cli.command("init-db")
    def init_db_command():
        db.create_all()
        print("Banco de dados inicializado com sucesso.")

    # Blueprints
    app.register_blueprint(user_bp, url_prefix="/users")

    @app.get("/")
    def home():
        return "API do NewsHub no ar! 🚀"

    return app