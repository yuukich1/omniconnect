class UserAlreadyExistsError(Exception):
    def __init__(self, message: str = "Пользователь с таким email уже существует"):
        self.message = message
        super().__init__(self.message)

class UserNotFoundError(Exception):
    def __init__(self, message: str = "Пользователь не найден"):
        self.message = message
        super().__init__(self.message)

class UserCredentialError(Exception):
    def __init__(self, message: str = "Неверный email или пароль"):
        self.message = message
        super().__init__(self.message)

class TokenPayloadError(Exception):
    def __init__(self, message: str = "В токене отсутствует идентификатор пользователя"):
        self.message = message
        super().__init__(self.message)
        
class CredentialTokenError(Exception):
    def __init__(self, message: str = 'Неверный токен'):
        self.message = message
        super().__init__(self.message)
        
class TokenExpiredError(Exception):
    def __init__(self, message: str = 'Токен истек'):
        self.message = message
        super().__init__(self.message)
        
class TokenInvalidError(Exception):
    def __init__(self, message: str = 'Токен не валидный'):
        self.message = message
        super().__init__(self.message)