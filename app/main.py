import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.webhooks import router as webhooks_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.agent import router as agent_router

app = FastAPI(
    title="PayAgentic Platform",
    description="Autonomous Agentic Commerce Engine for Google ADK & LoRA Licenses via PayPal",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تسجيل كافة المسارات تحت بادئة /api/v1
app.include_router(agent_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(webhooks_router, prefix="/api/v1")

if os.path.exists("dashboard"):
    app.mount("/static", StaticFiles(directory="dashboard"), name="static")

@app.get("/")
async def serve_dashboard():
    if os.path.exists("dashboard/index.html"):
        return FileResponse("dashboard/index.html")
    return {"message": "PayAgentic Engine Running"}

@app.get("/healthz")
async def health_check():
    return {"status": "healthy", "service": "PayAgentic-Core"}
