from fastapi import WebSocket
from loguru import logger

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_id: int):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)
        print(f"Сокет добавлен. Чат {chat_id} имеет {len(self.active_connections[chat_id])} подключений")

    def disconnect(self, websocket: WebSocket, chat_id: int):
        self.active_connections[chat_id].remove(websocket)
        if not self.active_connections[chat_id]:
            del self.active_connections[chat_id]

    async def broadcast(self, chat_id: int, message: dict):
        logger.info(f"Броадкаст в чат {chat_id}")
        if chat_id in self.active_connections:
            connections = self.active_connections[chat_id]
            logger.info(f"Найдено {len(connections)} сокетов для отправки")
            for connection in connections:
                await connection.send_json(message)

