from typing import Dict, List
import uuid

from fastapi import WebSocket


class ConnectionManager:
    
    def __init__(self):
        self.active_session: Dict[uuid.UUID, List[WebSocket]] = {}
        
    async def connect(self, websocket: WebSocket, chat_id: uuid.UUID):
        await websocket.accept()
        if chat_id not in self.active_session:
            self.active_session[chat_id] = []
        self.active_session[chat_id].append(websocket)
        
    def disconnect(self, websocket: WebSocket, chat_id: uuid.UUID):
        self.active_session[chat_id].remove(websocket)
        if not self.active_session[chat_id]:
            del self.active_session[chat_id]
            
    async def broadcast(self, chat_id: uuid.UUID, message: Dict):
        if chat_id in self.active_session:
            connection = self.active_session[chat_id]
            for connect in connection:
                await connect.send_json(message)