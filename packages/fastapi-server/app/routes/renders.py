"""Render-related endpoints"""
import os
from fastapi import APIRouter, HTTPException, status
from typing import Optional
from ..models.render import RenderMediaRequest, RenderMediaResponse, RenderStillRequest, RenderStillResponse
from ..models.common import JobStatusResponse, ListJobsResponse, JobStatus, CancelJobResponse
from ..services.queue import queue as render_queue

router = APIRouter()


def to_camel_case(snake_str: str) -> str:
    """Convert snake_case to camelCase"""
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def convert_dict_to_camel_case(data: dict) -> dict:
    """Convert all keys in a dictionary from snake_case to camelCase"""
    result = {}
    for key, value in data.items():
        camel_key = to_camel_case(key)
        # Handle nested objects like chromium_options and input_props
        if isinstance(value, dict):
            result[camel_key] = convert_dict_to_camel_case(value)
        else:
            result[camel_key] = value
    return result


def transform_serve_url(serve_url: str) -> str:
    """Transform localhost URLs to internal Docker service URLs

    Only transform localhost URLs to allow local development.
    Public URLs should be used as-is for production deployments.
    """
    # Get the internal frontend URL from environment
    internal_frontend_url = os.getenv("REMOTION_FRONTEND_URL", "http://remotion-frontend:3000")

    # Only transform localhost URLs for local development
    # Public URLs will work with bundle mode
    if "localhost" in serve_url or "127.0.0.1" in serve_url:
        print(f"DEBUG: Transforming localhost URL {serve_url} to {internal_frontend_url}", flush=True)
        return internal_frontend_url

    print(f"DEBUG: Using URL as-is: {serve_url}", flush=True)
    return serve_url


@router.post("/render/media", response_model=RenderMediaResponse)
async def render_media(request: RenderMediaRequest):
    """Submit a video render job"""
    try:
        options = request.model_dump(exclude_none=True)

        # Transform localhost URLs to internal Docker service URLs
        if "serve_url" in options:
            original_url = options["serve_url"]
            options["serve_url"] = transform_serve_url(original_url)
            print(f"DEBUG: Transformed URL from {original_url} to {options['serve_url']}", flush=True)

        # Ensure inputProps is an object, not None
        if "input_props" in options and options["input_props"] is None:
            options["input_props"] = {}

        # Debug: log inputProps before conversion
        print(f"DEBUG: input_props before conversion: {options.get('input_props')}", flush=True)

        # Convert codec enum to value
        if "codec" in options and hasattr(options["codec"], "value"):
            options["codec"] = options["codec"].value

        # Convert image_format enum to value
        if "image_format" in options and hasattr(options["image_format"], "value"):
            options["image_format"] = options["image_format"].value

        # Convert snake_case to camelCase for Node.js wrapper
        options = convert_dict_to_camel_case(options)

        # Debug: log after conversion
        print(f"DEBUG: inputProps after conversion: {options.get('inputProps')}", flush=True)

        job_id = await render_queue.enqueue("media", options)

        return RenderMediaResponse(
            job_id=job_id,
            status="queued",
            message="Render job queued successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/render/still", response_model=RenderStillResponse)
async def render_still(request: RenderStillRequest):
    """Submit a still image render job"""
    try:
        options = request.model_dump(exclude_none=True)

        # Transform localhost URLs to internal Docker service URLs
        if "serve_url" in options:
            original_url = options["serve_url"]
            options["serve_url"] = transform_serve_url(original_url)
            print(f"DEBUG: Transformed URL from {original_url} to {options['serve_url']}", flush=True)

        # Ensure inputProps is an object, not None
        if "input_props" in options and options["input_props"] is None:
            options["input_props"] = {}

        # Convert image_format enum to value
        if "image_format" in options and hasattr(options["image_format"], "value"):
            options["image_format"] = options["image_format"].value

        # Convert snake_case to camelCase for Node.js wrapper
        options = convert_dict_to_camel_case(options)

        job_id = await render_queue.enqueue("still", options)

        return RenderStillResponse(
            job_id=job_id,
            status="queued",
            message="Still render job queued successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """Get status of a render job"""
    job = render_queue.get_job(job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    return JobStatusResponse(**job.to_dict())


@router.delete("/jobs/{job_id}", response_model=CancelJobResponse)
async def cancel_job(job_id: str):
    """Cancel a render job"""
    success = await render_queue.cancel(job_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not cancel job"
        )

    job = render_queue.get_job(job_id)
    status = job.status if job else JobStatus.CANCELLED

    return CancelJobResponse(
        job_id=job_id,
        status=status,
        message="Job cancelled successfully"
    )


@router.get("/jobs", response_model=ListJobsResponse)
async def list_jobs(
    status: Optional[JobStatus] = None,
    limit: int = 100,
    offset: int = 0
):
    """List all render jobs"""
    jobs, total = render_queue.list_jobs(status, limit, offset)

    return ListJobsResponse(
        jobs=[JobStatusResponse(**job.to_dict()) for job in jobs],
        total=total,
        limit=limit,
        offset=offset
    )
