class BotPermissionError(Exception):
    def __init__(self, message="Bot not found or access denied"):
        self.message = message
        super().__init__(self.message)
        
class BotNotFoundError(Exception):
    def __init__(self, bot_id: int, message: str = 'unknown'):
        if message is None:
            message = f"Bot with id {bot_id} not found"
        self.message = message
        super().__init__(self.message)
        
class ChatNotFoundError(Exception):
    def __init__(self, chat_id: int, message: str = 'unknown'):
        if message is None:
            message = f"Chat with id {chat_id} not found"
        self.message = message
        super().__init__(self.message)