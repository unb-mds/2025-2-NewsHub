import logging
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.exceptions import UserValidationError, InvalidPasswordError, UserNotFoundError, EmailInUseError

class UserService:
    def __init__(self, repo: UserRepository | None = None):
        self.repo = repo or UserRepository()

    def register(self, data: dict) -> User:
        try:
            user_model = User(
                full_name=data["full_name"],
                email=data["email"],
                password=data["password"],
                birthdate=data.get("birthdate")
            )
        except (UserValidationError, InvalidPasswordError) as e:
            raise ValueError(str(e)) from e
        except KeyError as e:
            raise KeyError(f"Campo obrigatório ausente: {e}") from e

        if self.repo.find_by_email(user_model.email):
            raise EmailInUseError("E-mail já cadastrado")

        try:
            created_user = self.repo.create(user_model)
            return created_user
        except SQLAlchemyError:
            raise Exception("Ocorreu um erro ao registrar o usuário no banco de dados.")

    def login(self, data: dict) -> User | None:
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise ValueError("E-mail e senha são obrigatórios.")

        user = self.repo.find_by_email(email.lower())

        if user and user.verify_password(password):
            return user
        
        return None
    
    def get_profile(self, user_id: int) -> User | None:
        return self.repo.find_by_id(user_id)
    
    def update_profile(self, user_id: int, data: dict) -> User:
        user = self.repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundError("Usuário não encontrado")

        try:
            # Atribui os novos valores para acionar as validações do modelo
            if "full_name" in data:
                user.full_name = data["full_name"]
            if "birthdate" in data:
                birthdate_str = data.get("birthdate")
                if birthdate_str:
                    user.birthdate = date.fromisoformat(birthdate_str)
            if "email" in data:
                user.email = data["email"] # Isso acionará a validação de formato
                existing_user = self.repo.find_by_email(data["email"].lower())
                if existing_user and existing_user.id != user.id:
                    raise EmailInUseError("O novo e-mail já está em uso.")

        except UserValidationError as e:
            raise ValueError(str(e)) from e
        
        return self.repo.update(user)
    
    def change_password(self, user_id: int, data: dict):
        new_password = data.get("new_password")
        
        if not new_password:
            raise ValueError("Senha é obrigatório.")
        
        user = self.repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundError("Usuário não encontrado.")
        
        try:
            user.password = new_password
        except InvalidPasswordError as e:
            raise ValueError(str(e)) from e

        self.repo.update(user)
        