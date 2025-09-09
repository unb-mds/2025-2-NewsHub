import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Configurações
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecret")

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Registra a rota de usuario
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix="/users")

    @app.route("/")
    def home():
        return "API do NewsHub no ar! 🚀"

    return app

# CLI para inicializar banco
from flask.cli import with_appcontext
import click

@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()
    click.echo("Banco de dados inicializado!")
