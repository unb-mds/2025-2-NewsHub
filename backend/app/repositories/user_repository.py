from app.models.user import UserEntity, db

class UserRepository:
    @staticmethod
    def create(user: UserEntity) -> UserEntity:
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def find_by_email(email: str) -> UserEntity | None:
        stmt = db.select(UserEntity).filter_by(email=email)
        return db.session.execute(stmt).scalar_one_or_none()

    @staticmethod
    def list_all() -> list[UserEntity]:
        stmt = db.select(UserEntity)
        return db.session.execute(stmt).scalars().all()
