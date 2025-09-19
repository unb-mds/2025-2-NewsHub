# backend/app/repositories/users_topics_repository.py
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.entities.user_topic_entity import UserTopicEntity

class UsersTopicsRepository:
    def __init__(self, session=None):
        self.session = session or db.session

    def attach(self, user_id: int, topic_id: int) -> bool:
        try:
            exists = self.session.execute(
                select(UserTopicEntity).filter_by(user_id=user_id, topic_id=topic_id)
            ).scalar_one_or_none()
            if exists:
                return False
            rel = UserTopicEntity(user_id=user_id, topic_id=topic_id)
            self.session.add(rel)
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def detach(self, user_id: int, topic_id: int) -> bool:
        try:
            res = self.session.execute(
                delete(UserTopicEntity).filter_by(user_id=user_id, topic_id=topic_id)
            )
            self.session.commit()
            return res.rowcount > 0
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def list_user_topic_ids(self, user_id: int) -> list[int]:
        return self.session.execute(
            select(UserTopicEntity.topic_id).filter_by(user_id=user_id)
        ).scalars().all()
