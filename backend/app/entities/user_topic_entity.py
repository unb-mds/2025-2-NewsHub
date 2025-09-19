from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, UniqueConstraint
from app.extensions import db

class UserTopicEntity(db.Model):
    __tablename__ = "users_topics"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    created_at = mapped_column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "topic_id", name="uq_users_topics_user_topic"),
    )
