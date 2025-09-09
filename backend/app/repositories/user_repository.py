from app.models.user import User, db

class UserRepository:
    @staticmethod
    def create(user: User):
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def find_by_email(email: str):
        stmt = db.select(User).filter_by(email=email)
        return db.session.execute(stmt).scalar_one_or_none()

    @staticmethod
    def list_all():
        stmt = db.select(User)
        return db.session.execute(stmt).scalars().all()
