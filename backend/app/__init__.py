import os
from flask import Flask
from datetime import timedelta
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.extensions import db
from app.routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)

    CORS(app)
    
    # Carrega a chave secreta do JWT a partir das variáveis de ambiente.
    # É crucial que esta variável esteja definida no seu ambiente.
    # O uso de um fallback é removido para garantir que uma chave explícita seja sempre usada.
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_CSRF_PROTECT"] = True
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)


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
