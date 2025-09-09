from datetime import date
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(db.String(80), nullable=False)
    lastName: Mapped[str] = mapped_column(db.String(80), nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    birthdate: Mapped[Optional[date]] = mapped_column(db.Date, nullable=True)
    password_hash: Mapped[str] = mapped_column(db.String(200), nullable=False)

    def set_password(self, password: str) -> None:
        """Gera e armazena o hash da senha"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Valida a senha fornecida contra o hash salvo"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.email}>"
