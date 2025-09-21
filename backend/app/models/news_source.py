from datetime import datetime
from urllib.parse import urlparse
from app.entities.news_source_entity import NewsSourceEntity
from .exceptions import NewsSourceValidationError


class NewsSource:
    def __init__(self, name: str, url: str, id: int | None = None, created_at: datetime | None = None):
        self.id = id
        self.name = name
        self.url = url
        self.created_at = created_at

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not isinstance(value, str):
            raise NewsSourceValidationError("name", "não pode ser vazio.")
        name = " ".join(value.strip().split())
        if len(name) == 0 or len(name) > 255:
            raise NewsSourceValidationError("name", "tamanho inválido (1..255).")
        self._name = name

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str):
        if not value or not isinstance(value, str):
            raise NewsSourceValidationError("url", "não pode ser vazia.")
        if len(value) > 255:
            raise NewsSourceValidationError("url", "tamanho inválido (..255).")
        try:
            result = urlparse(value)
            if not all([result.scheme, result.netloc]):
                raise NewsSourceValidationError("url", "formato inválido.")
        except ValueError:
            raise NewsSourceValidationError("url", "formato inválido.")
        self._url = value

    @classmethod
    def from_entity(cls, entity: NewsSourceEntity) -> "NewsSource":
        if not entity:
            return None
        return cls(id=entity.id, name=entity.name, url=entity.url, created_at=entity.created_at)

    def to_orm(self) -> NewsSourceEntity:
        return NewsSourceEntity(id=self.id, name=self.name, url=self.url, created_at=self.created_at)