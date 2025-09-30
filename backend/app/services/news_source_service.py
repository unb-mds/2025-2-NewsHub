from app.repositories.news_source_repository import NewsSourceRepository
from app.repositories.user_news_source_repository import UserNewsSourceRepository
from app.models.exceptions import NewsSourceNotFoundError, NewsSourceAlreadyAttachedError
from sqlalchemy.exc import IntegrityError


class NewsSourceService():
    def __init__(self, repo: NewsSourceRepository | None = None, user_source_repo: UserNewsSourceRepository | None = None):
        self.repo = repo or NewsSourceRepository()
        self.user_source_repo = user_source_repo or UserNewsSourceRepository()

    def list_all(self):
        try:
            return self.repo.list_all()
        except Exception as e:
            raise

    def list_unassociated_by_user_id(self, user_id: int):
        try:
            return self.repo.list_unassociated_by_user_id(user_id)
        except Exception as e:
            raise

    def list_by_user_id(self, user_id: int):
        try:
            return self.repo.list_by_user_id(user_id)
        except Exception as e:
            raise

    def attach_source_to_user(self, user_id: int, source_id: int):
        if not self.repo.find_by_id(source_id):
            raise NewsSourceNotFoundError(f"Fonte de notícia com ID {source_id} não encontrada.")
        
        try:
            self.user_source_repo.attach(user_id, source_id)
        except IntegrityError as e:
            # Se o attach falhar por IntegrityError, pode ser que a associação já exista (race condition)
            # ou que o user_id/source_id seja inválido. O repo já lida com NewsSourceAlreadyAttachedError.
            raise e

    def detach_source_from_user(self, user_id: int, source_id: int):
        self.user_source_repo.detach(user_id, source_id)