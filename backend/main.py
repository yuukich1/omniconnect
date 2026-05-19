from fastapi import FastAPI
from src.api.v1.routers import all_routers
from src.api.v1.exception_handlers import register_exception_handlers


app = FastAPI(description='OmniConnect API')

for router in all_routers:
    app.include_router(router)
    
register_exception_handlers(app)