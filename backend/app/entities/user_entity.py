from datetime import date
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserEntity(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    firstName: Mapped[str] = mapped_column(db.String(80), nullable=False)
    lastName: Mapped[str] = mapped_column(db.String(80), nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    birthdate: Mapped[Optional[date]] = mapped_column(db.Date, nullable=True)
    password_hash: Mapped[str] = mapped_column(db.String(200), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.email}>"
