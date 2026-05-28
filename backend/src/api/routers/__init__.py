from .auth import router as auth_router
from .me import router as me_router
from .users import router as users_router
from .chats import router as chats_router


all_router = [
    auth_router,
    me_router,
    users_router,
    chats_router
]