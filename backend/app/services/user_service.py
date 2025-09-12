from app.entities.user_entity import UserEntity
from app.repositories.user_repository import UserRepository
from email_validator import validate_email, EmailNotValidError 

class UserService:
    def __init__(self, repo: UserRepository | None = None):
        self.repo = repo or UserRepository()

    def _validate_input(self, data: dict):
        try:
            valid_email = validate_email(data["email"], check_deliverability=False)
            email = valid_email.normalized
        except EmailNotValidError as e:
            raise ValueError(f"Formato de e-mail inválido: {e}") from e

        # 2. Validação de força da senha
        password = data.get("password")
        if not password or len(password) < 8: 
            raise ValueError("A senha deve ter pelo menos 8 caracteres")
        return email

    def register(self, data: dict) -> UserEntity:
        email = self._validate_input(data)

        if self.repo.find_by_email(email):
            raise ValueError("E-mail já cadastrado")

        user = UserEntity(
            full_name=data["full_name"], 
            email=email,
            birthdate=data.get("birthdate"),
        )
        user.set_password(data["password"])

        return self.repo.create(user)