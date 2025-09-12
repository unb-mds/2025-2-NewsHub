from sqlalchemy import select
from app.extensions import db
from app.entities.user_entity import UserEntity

class UserRepository:
    def __init__(self, session=None):
        self.session = session or db.session

    def create(self, user: UserEntity) -> UserEntity:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def find_by_email(self, email: str) -> UserEntity | None:
        stmt = select(UserEntity).filter_by(email=email)
        return self.session.execute(stmt).scalar_one_or_none()

    def list_all(self) -> list[UserEntity]:
        stmt = select(UserEntity)
        return list(self.session.execute(stmt).scalars().all())
