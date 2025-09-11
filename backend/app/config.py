import os
from flask import Flask
from app.extensions import db, bcrypt, jwt

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecret")

    db.init_app(app) 
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.entities import user_entity

    with app.app_context():
        db.create_all()

    # registrar rotas
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix="/users")

    @app.get("/")
    def home():
        return "API do NewsHub no ar! 🚀"

    return app
