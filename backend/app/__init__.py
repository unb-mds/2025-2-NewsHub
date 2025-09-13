import os
from flask import Flask
from flask_cors import CORS  # <-- 1. IMPORTE O CORS
from app.extensions import db
from app.routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)

    CORS(app)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init extensions
    db.init_app(app)

    # Importa modelos para registrar metadata
    from app.entities import user_entity  # noqa

    @app.cli.command("init-db")
    def init_db_command():
        """Cria as tabelas do banco de dados."""
        db.create_all()
        print("Banco de dados inicializado com sucesso.")

    # Blueprints
    app.register_blueprint(user_bp, url_prefix="/users")

    @app.get("/")
    def home():
        return "API do NewsHub no ar! 🚀"

    return app