from app.entities.user_entity import UserEntity
from app.repositories.user_repository import UserRepository
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import create_access_token 

class UserService:
    def __init__(self, repo: UserRepository | None = None):
        self.repo = repo or UserRepository()

    def _validate_input(self, data: dict):
        try:
            valid_email = validate_email(data["email"], check_deliverability=False)
            email = valid_email.normalized
        except EmailNotValidError as e:
            raise ValueError(f"Formato de e-mail inválido: {e}") from e

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
    
    def login(self, data: dict) -> str | None:
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise ValueError("E-mail e senha são obrigatórios.")

        user = self.repo.find_by_email(email)

        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return access_token
        
        return None