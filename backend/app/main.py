"""
AgentForge-Web FastAPI Application

Main entry point for the AgentForge web interface API.
Provides endpoints for AI agent execution and management.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# TODO: Import routers when implemented
# from .api import auth, agents
# from .core.config import settings

app = FastAPI(
    title="AgentForge Web API",
    description="Web interface for AgentForge AI agents",
    version="1.0.0"
)

# TODO: Configure CORS with settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Will be configured via settings
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Include routers
# app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
# app.include_router(agents.router, prefix="/api/agents", tags=["agents"])

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "agentforge-web"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AgentForge Web API", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
