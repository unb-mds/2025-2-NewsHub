import logging
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.entities.news_source_entity import NewsSourceEntity
from app.models.news_source import NewsSource

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
