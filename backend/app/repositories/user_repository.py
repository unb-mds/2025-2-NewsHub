from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.extensions import db
from app.entities.user_entity import UserEntity
from app.models.user import User

class UserRepository:
    def __init__(self, session=None):
        self.session = session or db.session

    def create(self, user_model: User) -> User:
        try:
            user_entity = user_model.to_orm()
            self.session.add(user_entity)
            self.session.commit()
            self.session.refresh(user_entity)
            return User.from_entity(user_entity)
        except SQLAlchemyError as e:
            logging.error(f"Erro de banco de dados ao criar usuário: {e}", exc_info=True)
            self.session.rollback()
            raise

    def find_by_email(self, email: str) -> User | None:
        stmt = select(UserEntity).where(func.lower(UserEntity.email) == email.lower())
        entity = self.session.execute(stmt).scalar_one_or_none()
        return User.from_entity(entity) if entity else None
    
    def find_by_id(self, user_id: int) -> User | None:
        stmt = select(UserEntity).where(UserEntity.id == user_id)
        entity = self.session.execute(stmt).scalar_one_or_none()
        return User.from_entity(entity) if entity else None

    def update(self, user_model: User) -> User:
        if not user_model.id:
            raise ValueError("O modelo de usuário deve ter um ID para ser atualizado.")
        
        try:
            user_entity = user_model.to_orm()
            updated_entity = self.session.merge(user_entity)
            self.session.commit()
            return User.from_entity(updated_entity)
        except SQLAlchemyError as e:
            logging.error(f"Erro de banco de dados ao atualizar usuário (ID: {user_model.id}): {e}", exc_info=True)
            self.session.rollback()
            raise
    
    def list_all(self) -> list[User]:
        stmt = select(UserEntity)
        entities = self.session.execute(stmt).scalars().all()
        return [User.from_entity(entity) for entity in entities]
