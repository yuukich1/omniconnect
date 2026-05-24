from typing import Optional


class BotPermissionError(Exception):
    def __init__(self, message="Bot not found or access denied"):
        self.message = message
        super().__init__(self.message)
        
class BotNotFoundError(Exception):
    def __init__(self, bot_id: Optional[int] = None, message: str = 'unknown'):
        if message is None:
            message = f"Bot with id {bot_id} not found"
        self.message = message
        super().__init__(self.message)


class WebhookCreateMessageError(Exception):
    def __init__(self, message: str | None = None):
        if message is None:
            message = f"Ошибка создания сообщения"
        self.message = message
        super().__init__(self.message)
        

class MediaGroupSendError(Exception):
    def __init__(self, message: str = 'Ошибка отправки медиа'):
        self.message = message
        super().__init__(self.message)