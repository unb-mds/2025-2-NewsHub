import os
from flask import Flask
from app.extensions import db, bcrypt, jwt
from datetime import timedelta
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from app.routes.user_routes import user_bp
from app.routes.topic_routes import topic_bp
from app.routes.news_source_routes import news_source_bp

def create_app(config_overrides=None):
    app = Flask(__name__)

    CORS(
        app,
        origins=["http://localhost:5173"],
        supports_credentials=True
    )
    
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_CSRF_PROTECT"] = True
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
    
    if config_overrides:
        app.config.update(config_overrides)

    SWAGGER_URL = '/api/docs' 
    API_URL = '/static/openapi.yaml'  

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Synapse API Documentation"
        }
    )
    app.register_blueprint(swaggerui_blueprint)

    from app.extensions import db
    db.init_app(app)
    jwt = JWTManager(app)

    from app.entities import (user_entity, topic_entity, user_topic_entity, 
                              news_entity, news_source_entity, news_topic_entity, user_news_sources_entity)
    
    with app.app_context():
        db.create_all()

    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(topic_bp, url_prefix="/topics")
    app.register_blueprint(news_source_bp, url_prefix="/news_sources")

    return app
