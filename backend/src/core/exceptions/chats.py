
class ChatNotFoundError(Exception):
    def __init__(self, chat_id: int):
        self.message = f"Chat with id {chat_id} not found"
        super().__init__(self.message)
        
    