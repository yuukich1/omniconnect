from .v1.auth import router as auth_router
from .v1.bots import router as bots_router
from .webhook.telegram import router as telegram_webhook
from .v1.chats import router as chats_router
from .v1.messages import router as messages_router

all_routers = [
    auth_router,
    bots_router,
    telegram_webhook,
    chats_router,
    messages_router
]

