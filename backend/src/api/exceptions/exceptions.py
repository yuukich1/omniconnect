class BaseDomainException(Exception):
    def __init__(self, message: str, code: str = "DOMAIN_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class AlreadyExistsError(BaseDomainException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, code="ALREADY_EXISTS")

class ForeignKeyError(BaseDomainException):
    def __init__(self, message: str = "Related resource not found"):
        super().__init__(message, code="FOREIGN_KEY_VIOLATION")

class DataIntegrityError(BaseDomainException):
    def __init__(self, message: str = "Data integrity violation"):
        super().__init__(message, code="DATA_INTEGRITY_VIOLATION")
        
class AuthenticationError(BaseDomainException):
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message, code="AUTHENTICATION_ERROR")
        
class AuthorizationError(BaseDomainException):
    def __init__(self, message: str = "Not enough permissions"):
        super().__init__(message, code="AUTHORIZATION_ERROR")
        
class NotFoundError(BaseDomainException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, code="NOT_FOUND")