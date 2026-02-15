"""Render-related endpoints"""
from fastapi import APIRouter, HTTPException, status
from typing import Optional
from ..models.render import RenderMediaRequest, RenderMediaResponse, RenderStillRequest, RenderStillResponse
from ..models.common import JobStatusResponse, ListJobsResponse, JobStatus, CancelJobResponse
from ..services.queue import queue as render_queue

router = APIRouter()


@router.post("/render/media", response_model=RenderMediaResponse)
async def render_media(request: RenderMediaRequest):
    """Submit a video render job"""
    try:
        options = request.model_dump(exclude_none=True)

        # Convert codec enum to value
        if "codec" in options and hasattr(options["codec"], "value"):
            options["codec"] = options["codec"].value

        # Convert image_format enum to value
        if "image_format" in options and hasattr(options["image_format"], "value"):
            options["image_format"] = options["image_format"].value

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

        # Convert image_format enum to value
        if "image_format" in options and hasattr(options["image_format"], "value"):
            options["image_format"] = options["image_format"].value

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
