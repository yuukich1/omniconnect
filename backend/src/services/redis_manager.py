import json
from loguru import logger
from typing import Any
from redis.asyncio import Redis, RedisError

class RedisMessageBroker:
    def __init__(self, host: str, port: int, db: int = 0):
        self.client = Redis(
            host=host, 
            port=port, 
            db=db, 
            decode_responses=True,
            socket_connect_timeout=5
        )

    async def publish(self, channel: Any, message: dict):
        try:
            await self.client.publish(str(channel), json.dumps(message))
        except RedisError as e:
            logger.error(f"Failed to publish to {channel}: {e}")
            raise 

    async def get_pubsub(self):
        return self.client.pubsub()