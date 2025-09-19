# backend/app/services/topic_service.py
from sqlalchemy.exc import IntegrityError
from app.models.topic import Topic
from app.repositories.topic_repository import TopicRepository
from app.repositories.users_topics_repository import UsersTopicsRepository

class TopicService:
    def __init__(self, topic_repo: TopicRepository | None = None, users_topics_repo: UsersTopicsRepository | None = None):
        self.topics = topic_repo or TopicRepository()
        self.users_topics = users_topics_repo or UsersTopicsRepository()

    def create_and_attach(self, user_id: int, data: dict) -> dict:
        name = (data or {}).get("name")
        state = (data or {}).get("state", 1)
        topic = Topic(name=name, state=state)
        existing = self.topics.find_by_name(topic.name)
        if existing:
            attached = self.users_topics.attach(user_id, existing.id)
            return {"topic": existing, "attached": attached}
        try:
            created = self.topics.create(topic)
        except IntegrityError:
            created = self.topics.find_by_name(topic.name) or None
            if not created:
                raise
        attached = self.users_topics.attach(user_id, created.id)
        return {"topic": created, "attached": attached}
    
    def create_topic(self, data: dict) -> Topic:
        name = (data or {}).get("name")
        state = (data or {}).get("state", 1)
        topic = Topic(name=name, state=state)
        try:
            created = self.topics.create(topic)
        except IntegrityError:
            created = self.topics.find_by_name(topic.name) or None
            if not created:
                raise
        return {"topic": created}

    def find_by_user(self, user_id: int):
        ids = self.users_topics.list_user_topic_ids(user_id)
        return [self.topics.find_by_id(tid) for tid in ids if tid is not None]

    def detach_for_user(self, user_id: int, topic_id: int) -> bool:
        return self.users_topics.detach(user_id, topic_id)
