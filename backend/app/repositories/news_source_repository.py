import logging
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.entities.news_source_entity import NewsSourceEntity
from app.models.news_source import NewsSource
from app.entities.user_news_sources_entity import UserNewsSourceEntity

class NewsSourceRepository:
    def __init__(self, session=None):
        self.session = session or db.session

    def create(self, model: NewsSource) -> NewsSource:
        try:
            entity = model.to_orm()
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return NewsSource.from_entity(entity)
        except SQLAlchemyError as e:
            logging.error(f"Erro de banco ao criar fonte de notícia: {e}", exc_info=True)
            self.session.rollback()
            raise

    def find_by_id(self, source_id: int) -> NewsSource | None:
        try:
            entity = self.session.get(NewsSourceEntity, source_id)
            return NewsSource.from_entity(entity) if entity else None
        except SQLAlchemyError as e:
            logging.error(f"Erro de banco ao buscar fonte por ID: {e}", exc_info=True)
            raise

    def find_by_name(self, name: str) -> NewsSource | None:
        try:
            stmt = select(NewsSourceEntity).where(func.lower(NewsSourceEntity.name) == name.lower())
            entity = self.session.execute(stmt).scalar_one_or_none()
            return NewsSource.from_entity(entity) if entity else None
        except SQLAlchemyError as e:
            logging.error(f"Erro de banco ao buscar fonte por nome: {e}", exc_info=True)
            raise

    def find_by_url(self, url: str) -> NewsSource | None:
        try:
            stmt = select(NewsSourceEntity).where(NewsSourceEntity.url == url)
            entity = self.session.execute(stmt).scalar_one_or_none()
            return NewsSource.from_entity(entity) if entity else None
        except SQLAlchemyError as e:
            logging.error(f"Erro de banco ao buscar fonte por URL: {e}", exc_info=True)
            raise

    def list_all(self) -> list[NewsSource]:
        try:
            stmt = select(NewsSourceEntity).order_by(NewsSourceEntity.name)
            entities = self.session.execute(stmt).scalars().all()
            return [NewsSource.from_entity(e) for e in entities]
        except SQLAlchemyError as e:
            logging.error(f"Erro de banco ao listar fontes de notícias: {e}", exc_info=True)
            raise

    def list_by_user_id(self, user_id: int) -> list[NewsSource]:
        try:
            stmt = (
                select(NewsSourceEntity)
                .join(UserNewsSourceEntity, UserNewsSourceEntity.source_id == NewsSourceEntity.id)
                .where(UserNewsSourceEntity.user_id == user_id)
                .order_by(NewsSourceEntity.name)
            )
            entities = self.session.execute(stmt).scalars().all()
            return [NewsSource.from_entity(e) for e in entities]
        except SQLAlchemyError as e:
            logging.error(f"Erro de banco ao listar fontes de notícias por usuário: {e}", exc_info=True)
            raise

    def list_unassociated_by_user_id(self, user_id: int) -> list[NewsSource]:
        try:
            subquery = select(UserNewsSourceEntity.source_id).where(UserNewsSourceEntity.user_id == user_id)

            stmt = (
                select(NewsSourceEntity)
                .where(NewsSourceEntity.id.notin_(subquery))
                .order_by(NewsSourceEntity.name)
            )
            entities = self.session.execute(stmt).scalars().all()
            return [NewsSource.from_entity(e) for e in entities]
        except SQLAlchemyError as e:
            logging.error(f"Erro de banco ao listar fontes não associadas ao usuário: {e}", exc_info=True)
            raise
