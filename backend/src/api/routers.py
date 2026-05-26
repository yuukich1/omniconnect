from .v1.auth import router as auth_router
from .v1.bots import router as bots_router
from .webhook.telegram import webhook as telegram_webhook
from .v1.chats import router as chats_router
from .v1.messages import router as messages_router
from .websokets.message import websoket as message_websocket
from .v1.users import router as users_router
from .v1.post import router as post_router
all_routers = [
    auth_router,
    bots_router,
    chats_router,
    messages_router,
    users_router,
    post_router
]

all_webhooks = [
    telegram_webhook
]

all_websokets = [
    message_websocket
]