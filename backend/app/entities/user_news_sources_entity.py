from datetime import datetime
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db

class UserNewsSourceEntity(db.Model):
    __tablename__ = "user_news_sources"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("news_sources.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    created_at = mapped_column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    
    __table_args__ = (
        UniqueConstraint("user_id", "source_id", name="uq_user_news_sources_user_source"),
    )
