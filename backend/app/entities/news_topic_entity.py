from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, UniqueConstraint
from app.extensions import db

class NewsTopicEntity(db.Model):
    __tablename__ = "news_topics"

    news_id: Mapped[int] = mapped_column(ForeignKey("news.id", ondelete="CASCADE"), primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True)
    created_at = mapped_column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("news_id", "topic_id", name="uq_news_topics_news_topic"),
    )