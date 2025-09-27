# backend/app/repositories/topic_repository.py
import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.entities.topic_entity import TopicEntity
from app.models.topic import Topic

class TopicRepository:
    def __init__(self, session=None):
        self.session = session or db.session

    def create(self, model: Topic) -> Topic:
        try:
            model.name = model.name.lower()
            entity = model.to_orm()
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return Topic.from_entity(entity)
        except SQLAlchemyError as e:
            logging.error(f"Erro de banco ao criar tópico: {e}", exc_info=True)
            self.session.rollback()
            raise

    def find_by_name(self, name: str) -> Topic | None:
        stmt = select(TopicEntity).filter(TopicEntity.name == name.lower())
        e = self.session.execute(stmt).scalar_one_or_none()
        return Topic.from_entity(e) if e else None

    def find_by_id(self, topic_id: int) -> Topic | None:
        stmt = select(TopicEntity).filter_by(id=topic_id)
        e = self.session.execute(stmt).scalar_one_or_none()
        return Topic.from_entity(e) if e else None

    def list_all(self) -> list[Topic]:
        stmt = select(TopicEntity)
        es = self.session.execute(stmt).scalars().all()
        return [Topic.from_entity(e) for e in es]
