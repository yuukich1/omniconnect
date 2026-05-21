class ChatNotFoundError(Exception):
    def __init__(self, chat_id: int, message: str = 'unknown'):
        if message is None:
            message = f"Chat with id {chat_id} not found"
        self.message = message
        super().__init__(self.message)
        