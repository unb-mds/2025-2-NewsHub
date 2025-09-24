import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.entities.news_entity import NewsEntity
from app.models.news import News

class NewsRepository:
    def __init__(self, session=None):
        self.session = session or db.session

    def create(self, model: News) -> News:
        try:
            entity = model.to_orm()
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return News.from_entity(entity)
        except SQLAlchemyError as e:
            logging.error(f"Erro de banco ao criar notícia: {e}", exc_info=True)
            self.session.rollback()
            raise

    def find_by_id(self, news_id: int) -> News | None:
        try:
            entity = self.session.get(NewsEntity, news_id)
            return News.from_entity(entity) if entity else None
        except SQLAlchemyError as e:
            logging.error(f"Erro de banco ao buscar notícia por ID: {e}", exc_info=True)
            raise

    def find_by_url(self, url: str) -> News | None:
        try:
            stmt = select(NewsEntity).where(NewsEntity.url == url)
            entity = self.session.execute(stmt).scalar_one_or_none()
            return News.from_entity(entity) if entity else None
        except SQLAlchemyError as e:
            logging.error(f"Erro de banco ao buscar notícia por URL: {e}", exc_info=True)
            raise

    def list_all(self, page: int = 1, per_page: int = 20) -> list[News]:
        try:
            stmt = (
                select(NewsEntity)
                .order_by(NewsEntity.published_at.desc())
                .offset((page - 1) * per_page)
                .limit(per_page)
            )
            entities = self.session.execute(stmt).scalars().all()
            return [News.from_entity(e) for e in entities]
        except SQLAlchemyError as e:
            logging.error(f"Erro de banco ao listar notícias: {e}", exc_info=True)
            raise
