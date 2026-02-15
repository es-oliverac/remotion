"""FastAPI application entry point"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

from .config import settings
from .routes import renders, compositions, health
from .services.queue import RenderQueue
from .services.storage import storage


# Global queue instance
queue: RenderQueue


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    global queue
    queue = RenderQueue(max_concurrent=settings.MAX_CONCURRENT_RENDERS)
    await queue.start()

    # Make queue available to routes
    import app.routes.renders
    app.routes.renders.render_queue = queue

    storage.ensure_output_dir()

    yield

    # Shutdown
    await queue.stop()


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="HTTP API for Remotion video rendering",
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for outputs
app.mount("/outputs", StaticFiles(directory=settings.OUTPUT_DIR), name="outputs")

# Include routers
app.include_router(renders.router, prefix=settings.API_PREFIX, tags=["renders"])
app.include_router(compositions.router, prefix=settings.API_PREFIX, tags=["compositions"])
app.include_router(health.router, prefix=settings.API_PREFIX, tags=["health"])


# WebSocket for progress updates
@app.websocket("/api/v1/jobs/{job_id}/progress")
async def job_progress(websocket: WebSocket, job_id: str):
    """WebSocket endpoint for real-time progress updates"""
    await websocket.accept()

    job = queue.get_job(job_id)
    if not job:
        await websocket.close(code=1008, reason="Job not found")
        return

    try:
        # Send initial status
        await websocket.send_json(job.to_dict())

        # Keep connection open and send updates
        while job.status in ["queued", "in-progress"]:
            await asyncio.sleep(0.5)
            await websocket.send_json(job.to_dict())

        # Send final status
        await websocket.send_json(job.to_dict())

    except WebSocketDisconnect:
        pass
    finally:
        await websocket.close()
