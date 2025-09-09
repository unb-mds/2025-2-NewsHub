from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from app.models.user import db, User

def create_user():
    data = request.get_json()

    try:
        user = User(
            nome=data["nome"],
            lastName=data["lastName"],
            email=data["email"],
            birthdate=data.get("birthdate")
        )
        user.set_password(data["senha"])

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Usuário criado com sucesso!"}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "E-mail já cadastrado"}), 409
    except KeyError as e:
        return jsonify({"error": f"Campo obrigatório ausente: {e}"}), 400
