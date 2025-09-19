from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db

class TopicEntity(db.Model):
    __tablename__ = "topics"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    state: Mapped[int] = mapped_column(db.SmallInteger, nullable=False, default=0)
    name: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    created_at = mapped_column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, UniqueConstraint
from app.extensions import db
