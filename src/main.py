import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.core.config import settings
from src.gateway.router import router as gateway_router
from src.hitl.router import router as hitl_router
from src.api.admin_routes import router as admin_router
from src.api.websocket import ws_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Dynamic Risk-Aware Security Framework for Model Context Protocol"
)

app.include_router(gateway_router)
app.include_router(hitl_router)
app.include_router(admin_router)
app.include_router(ws_router)

# Mount static files for dashboard UI
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/dashboard")
@app.get("/")
async def serve_dashboard():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"status": "ok", "service": settings.PROJECT_NAME}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME, "version": settings.VERSION}
