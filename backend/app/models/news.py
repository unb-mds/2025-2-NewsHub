from datetime import datetime
from urllib.parse import urlparse
from app.entities.news_entity import NewsEntity
from .exceptions import NewsValidationError


class News:
    def __init__(
        self,
        title: str,
        url: str,
        published_at: datetime,
        source_id: int,
        content: str,
        id: int | None = None,
        description: str | None = None,
        image_url: str | None = None,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.url = url
        self.image_url = image_url
        self.content = content
        self.published_at = published_at
        self.source_id = source_id
        self.created_at = created_at

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not isinstance(value, str):
            raise NewsValidationError("title", "não pode ser vazio.")
        title = " ".join(value.strip().split())
        if len(title) == 0:
            raise NewsValidationError("title", "não pode ser vazio.")
        self._title = title

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str):
        if not value or not isinstance(value, str):
            raise NewsValidationError("url", "não pode ser vazia.")
        if not isinstance(value, str):
            raise NewsValidationError("url", "deve ser uma string.")
        if len(value) > 500:
            raise NewsValidationError("url", "tamanho inválido (..500).")
        try:
            result = urlparse(value)
            if not all([result.scheme, result.netloc]):
                raise NewsValidationError("url", "formato inválido.")
        except ValueError:
            raise NewsValidationError("url", "formato inválido.")
        self._url = value

    @property
    def image_url(self) -> str | None:
        return self._image_url

    @image_url.setter
    def image_url(self, value: str | None):
        if value is None:
            self._image_url = None
            return
        try:
            parsed = urlparse(value)
            if not all([parsed.scheme, parsed.netloc]) or len(value) > 500:
                raise NewsValidationError("image_url", "formato ou tamanho inválido.")
        except ValueError:
            raise NewsValidationError("image_url", "formato inválido.")
        self._image_url = value

    @property
    def published_at(self) -> datetime:
        return self._published_at

    @published_at.setter
    def published_at(self, value: datetime):
        if not value or not isinstance(value, datetime):
            raise NewsValidationError("published_at", "deve ser um datetime válido.")
        self._published_at = value

    @property
    def source_id(self) -> int:
        return self._source_id

    @source_id.setter
    def source_id(self, value: int):
        if not value or not isinstance(value, int) or value <= 0:
            raise NewsValidationError("source_id", "deve ser um inteiro positivo.")
        self._source_id = value

    @classmethod
    def from_entity(cls, entity: NewsEntity) -> "News":
        if not entity:
            return None
        return cls(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            url=entity.url,
            image_url=entity.image_url,
            content=entity.content,
            published_at=entity.published_at,
            source_id=entity.source_id,
            created_at=entity.created_at,
        )

    def to_orm(self) -> NewsEntity:
        return NewsEntity(
            id=self.id,
            title=self.title,
            description=self.description,
            url=self.url,
            image_url=self.image_url,
            content=self.content,
            published_at=self.published_at,
            source_id=self.source_id,
            created_at=self.created_at,
        )