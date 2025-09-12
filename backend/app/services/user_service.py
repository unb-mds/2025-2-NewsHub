from app.entities.user_entity import UserEntity
from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, repo: UserRepository | None = None):
        self.repo = repo or UserRepository()

    def register(self, data: dict) -> UserEntity:
        email = data["email"].strip().lower()
        if self.repo.find_by_email(email):
            raise ValueError("E-mail já cadastrado")

        user = UserEntity(
            full_name=data["full_name"],
            email=email,
            birthdate=data.get("birthdate"),
        )
        # alinhar com payload do frontend: "password"
        user.set_password(data["password"])

        return self.repo.create(user)
