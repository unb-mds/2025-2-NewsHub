# backend/app/models/topic.py
from datetime import datetime
from app.entities.topic_entity import TopicEntity

class TopicValidationError(ValueError):
    def __init__(self, field: str, message: str):
        super().__init__(f"{field}: {message}")

class Topic:
    def __init__(self, name: str, state: int = 0, id: int | None = None, created_at: datetime | None = None):
        self.id = id
        self.name = self._validate_name(name)
        self.state = self._validate_state(state)
        self.created_at = created_at

    def _validate_name(self, value: str) -> str:
        if not value or not isinstance(value, str):
            raise TopicValidationError("name", "não pode ser vazio.")
        name = " ".join(value.strip().split())
        if len(name) == 0 or len(name) > 255:
            raise TopicValidationError("name", "tamanho inválido (1..255).")
        return name

    def _validate_state(self, v: int) -> int:
        try:
            iv = int(v)
        except Exception:
            raise TopicValidationError("state", "deve ser inteiro.")
        if iv < 0 or iv > 32767:
            raise TopicValidationError("state", "fora do intervalo de SMALLINT.")
        return iv

    @classmethod
    def from_entity(cls, e: TopicEntity) -> "Topic":
        if not e:
            return None
        return cls(id=e.id, name=e.name, state=e.state, created_at=e.created_at)

    def to_orm(self) -> TopicEntity:
        return TopicEntity(id=self.id, name=self.name, state=self.state, created_at=self.created_at)
