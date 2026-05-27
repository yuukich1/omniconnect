from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from src.api.routers import all_routers, all_webhooks, all_websokets
from src.api.exception_handlers import register_exception_handlers
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(description='OmniConnect API', docs_url=None, redoc_url=None)

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

@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="OmniConnect API",
    )

for router in all_routers:
    app.include_router(prefix='/api/v0.1', router=router)
    
for webhook in all_webhooks:
    app.include_router(router=webhook)
    
for websocket in all_websokets:
    app.include_router(prefix='/ws', router=websocket)
    
register_exception_handlers(app)


app.mount("/static", StaticFiles(directory="D:/nya/yuuki/OmniConnect/backend/uploads"), name="static")
