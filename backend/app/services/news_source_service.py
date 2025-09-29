from app.repositories.news_source_repository import NewsSourceRepository
from app.repositories.user_news_source_repository import UserNewsSourceRepository
from app.models.exceptions import NewsSourceNotFoundError
from sqlalchemy.exc import IntegrityError


class NewsSourceService():
    def __init__(self):
        self.repo = NewsSourceRepository()
        self.user_source_repo = UserNewsSourceRepository()

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
        except IntegrityError:
            # Se ainda houver um IntegrityError, pode ser um problema com o user_id
            # ou uma race condition que o `attach` não pegou.
            # O controlador pode tratar isso como um 404 ou 409.
            raise

    def detach_source_from_user(self, user_id: int, source_id: int):
        self.user_source_repo.detach(user_id, source_id)