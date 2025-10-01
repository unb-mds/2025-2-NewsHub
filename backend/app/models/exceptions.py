class DomainError(Exception):
    """Classe base para erros de domínio específicos da aplicação."""
    pass

class UserValidationError(DomainError):
    """Lançado quando um atributo do usuário falha na validação."""
    def __init__(self, attribute: str, message: str):
        self.attribute = attribute
        self.message = message
        super().__init__(f"Erro de validação em '{attribute}': {message}")

class InvalidPasswordError(UserValidationError):
    """Lançado para erros de validação específicos da senha."""
    def __init__(self, message: str):
        super().__init__("password", message)

class UserNotFoundError(DomainError):
    """Lançado quando um usuário não é encontrado no banco de dados."""
    pass

class EmailInUseError(DomainError):
    """Lançado quando um e-mail já está em uso por outro usuário."""
    pass

class NewsSourceValidationError(DomainError):
    def __init__(self, field: str, message: str):
        super().__init__(f"{field}: {message}")

class NewsValidationError(DomainError):
    def __init__(self, field: str, message: str):
        super().__init__(f"{field}: {message}")

class NewsSourceNotFoundError(DomainError):
    """Lançado quando uma fonte de notícia não é encontrada."""
    pass

class NewsSourceAlreadyAttachedError(DomainError):
    """Lançado quando se tenta associar uma fonte que já está associada ao usuário."""
    pass

class NewsSourceNotAttachedError(DomainError):
    """Lançado quando se tenta desassociar uma fonte que não está associada."""
    pass
