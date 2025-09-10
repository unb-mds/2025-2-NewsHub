from app.models.user import UserEntity
from app.repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def register(data: dict) -> UserEntity:
        if UserRepository.find_by_email(data["email"]):
            raise ValueError("E-mail já cadastrado")

        user = UserEntity(
            firstName=data["firstName"],
            lastName=data["lastName"],
            email=data["email"],
            birthdate=data.get("birthdate")
        )
        user.set_password(data["senha"])

        return UserRepository.create(user)
