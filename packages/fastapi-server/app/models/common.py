"""Common data models"""
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional, List


class JobStatus(str, Enum):
    """Status of a render job"""
    QUEUED = "queued"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RenderProgress(BaseModel):
    """Progress information for a render job"""
    rendered_frames: int
    encoded_frames: int
    progress: float
    stitch_stage: Optional[str] = None


class JobStatusResponse(BaseModel):
    """Response model for job status"""
    job_id: str
    status: JobStatus
    progress: float = 0.0
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    output_url: Optional[str] = None
    output_path: Optional[str] = None
    error: Optional[str] = None
    render_progress: Optional[RenderProgress] = None


class ListJobsResponse(BaseModel):
    """Response model for listing jobs"""
    jobs: List[JobStatusResponse]
    total: int
    limit: int = 100
    offset: int = 0


class CancelJobResponse(BaseModel):
    """Response model for cancelling a job"""
    job_id: str
    status: JobStatus
    message: str
