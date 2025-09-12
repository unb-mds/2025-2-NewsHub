import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy import text # Importe a função text

# Inicializa a extensão, mas não a conecta a uma aplicação ainda
db = SQLAlchemy()

# --- Modelos de Dados (representam tabelas no banco) ---
# Mova os modelos para o escopo global para que o SQLAlchemy os registre.
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Article {self.title}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

def create_app():
    """Cria e configura uma instância da aplicação Flask."""
    app = Flask(__name__)

    # --- Configuração do Banco de Dados ---
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL não está configurada.")

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Associa a extensão SQLAlchemy com a aplicação
    db.init_app(app)

    # --- Rotas da API ---
    @app.route('/')
    def hello_world():
        return 'API do NewsHub no ar! Pronta para testes.'

    @app.route('/health-check')
    def health_check():
        try:
            # Envolva a string SQL com a função text()
            db.session.execute(text('SELECT 1'))
            return jsonify({
                "status": "ok",
                "message": "A conexão com o banco de dados PostgreSQL está funcionando!"
            })
        except (OperationalError, Exception) as e:
            # Retorna uma resposta de erro clara em caso de falha
            return jsonify({
                "status": "error",
                "message": "Falha na conexão com o banco de dados.",
                "details": str(e)
            }), 500

    # NOVAS ROTAS: /users
    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        if not data or not 'username' in data:
            return jsonify({"error": "O nome de usuário é obrigatório"}), 400

        # Verifica se o usuário já existe para evitar duplicatas
        if db.session.query(User).filter_by(username=data['username']).first():
            return jsonify({"error": "Este nome de usuário já existe"}), 409

        new_user = User(username=data['username'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuário criado com sucesso!", "user": new_user.username}), 201

    @app.route('/users', methods=['GET'])
    def get_users():
        try:
            users = db.session.query(User).all()
            usernames = [user.username for user in users]
            return jsonify(users=usernames)
        except Exception as e:
            # Pode ocorrer um erro se a tabela ainda não existir, por exemplo
            return jsonify({"error": "Erro ao buscar usuários", "details": str(e)}), 500

    return app

# Cria a instância da aplicação para que o Gunicorn possa encontrá-la
app = create_app()

# --- Comando CLI para inicializar o banco de dados ---
@app.cli.command("init-db")
def init_db_command():
    """Cria as tabelas do banco de dados."""
    db.create_all()
    print("Banco de dados inicializado e tabelas criadas.")