from fastapi import FastAPI
from src.api.routers import all_routers
from src.api.exception_handlers import register_exception_handlers


app = FastAPI(description='OmniConnect API')

for router in all_routers:
    app.include_router(prefix='/api/v1', router=router)
    
register_exception_handlers(app)