import logging
from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.extensions import db
from app.entities.user_news_sources_entity import UserNewsSourceEntity
from app.models.exceptions import NewsSourceAlreadyAttachedError, NewsSourceNotAttachedError

class UserNewsSourceRepository:
    def __init__(self, session=None):
        self.session = session or db.session

    def attach(self, user_id: int, source_id: int):
        try:
            # Verifica se a relação já existe
            exists_stmt = select(UserNewsSourceEntity).where(UserNewsSourceEntity.user_id == user_id, UserNewsSourceEntity.source_id == source_id)
            if self.session.execute(exists_stmt).scalar_one_or_none():
                raise NewsSourceAlreadyAttachedError("A fonte de notícia já está associada a este usuário.")

            new_attachment = UserNewsSourceEntity(user_id=user_id, source_id=source_id)
            self.session.add(new_attachment)
            self.session.commit()
        except IntegrityError: # Caso a fonte ou usuário não exista, ou race condition
            self.session.rollback()
            logging.warning(f"Falha de integridade ao tentar associar usuário {user_id} com fonte {source_id}.")
            # Re-lança como uma exceção mais genérica, pois pode ser usuário ou fonte inexistente.
            # O serviço pode tratar isso melhor.
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            logging.error(f"Erro de banco ao associar fonte a usuário: {e}", exc_info=True)
            raise

    def detach(self, user_id: int, source_id: int):
        try:
            stmt = delete(UserNewsSourceEntity).where(UserNewsSourceEntity.user_id == user_id, UserNewsSourceEntity.source_id == source_id)
            result = self.session.execute(stmt)
            self.session.commit()
            if result.rowcount == 0:
                raise NewsSourceNotAttachedError("Associação não encontrada para ser removida.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logging.error(f"Erro de banco ao desassociar fonte de usuário: {e}", exc_info=True)
            raise