from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Text
from app.extensions import db

class NewsEntity(db.Model):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(db.String(500), unique=True, nullable=False)
    image_url: Mapped[str] = mapped_column(db.String(500), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False) 
    published_at: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), nullable=False)
    
    source_id: Mapped[int] = mapped_column(ForeignKey("news_sources.id"), nullable=False)
    
    created_at = mapped_column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)