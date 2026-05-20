from fastapi import FastAPI
from src.api.routers import all_routers
from src.api.exception_handlers import register_exception_handlers
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(description='OmniConnect API')

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,     
    allow_methods=["*"],
    allow_headers=["*"],              
)

for router in all_routers:
    app.include_router(prefix='/api/v1', router=router)
    
register_exception_handlers(app)