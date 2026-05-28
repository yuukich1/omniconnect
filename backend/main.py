from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from src.api import all_router, register_exception_handlers, all_websockets

app = FastAPI(description='OmniConnect API', docs_url=None, redoc_url=None)

@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="OmniConnect API",
    )

for router in all_router:
    app.include_router(prefix='/api/v0.2', router=router)

for websocket in all_websockets:
    app.include_router(prefix='/ws/v0.2', router=websocket)
    
register_exception_handlers(app)
    