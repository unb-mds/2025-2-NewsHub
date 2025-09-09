from app.models.user import User
from app.repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def register(data):
        if UserRepository.find_by_email(data["email"]):
            raise ValueError("E-mail já cadastrado")

        user = User(
            nome=data["nome"],
            lastName=data["lastName"],
            email=data["email"],
            birthdate=data.get("birthdate")  # pode ser opcional
        )
        user.set_password(data["senha"])

        return UserRepository.create(user)
