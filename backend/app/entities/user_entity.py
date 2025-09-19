from datetime import date
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db

class UserEntity(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(db.String(80), nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    birthdate: Mapped[Optional[date]] = mapped_column(db.Date, nullable=True)
    password_hash: Mapped[str] = mapped_column(db.String(200), nullable=False)

