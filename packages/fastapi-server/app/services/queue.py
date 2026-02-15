"""Async job queue for rendering tasks"""
import asyncio
import uuid
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass, field
from enum import Enum

from .renderer import NodeRenderer
from .storage import storage


class JobStatus(str, Enum):
    """Status of a render job"""
    QUEUED = "queued"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Job:
    """Represents a render job"""
    id: str
    type: str  # "media" or "still"
    options: dict
    status: JobStatus = JobStatus.QUEUED
    progress: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    output_path: Optional[str] = None
    output_url: Optional[str] = None
    error: Optional[str] = None
    cancel_requested: bool = False

    def to_dict(self) -> dict:
        """Convert job to dictionary"""
        return {
            "job_id": self.id,
            "status": self.status,
            "progress": self.progress,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "output_url": self.output_url,
            "output_path": self.output_path,
            "error": self.error
        }


class RenderQueue:
    """Async job queue for rendering tasks"""

    def __init__(self, max_concurrent: int = 2):
        self.jobs: Dict[str, Job] = {}
        self.queue: asyncio.Queue = asyncio.Queue()
        self.max_concurrent = max_concurrent
        self.active_tasks: set = set()
        self.renderer = NodeRenderer()
        self._workers: List[asyncio.Task] = []
        self._running = False

    async def start(self):
        """Start queue workers"""
        if self._running:
            return

        self._running = True
        for i in range(self.max_concurrent):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self._workers.append(worker)

    async def stop(self):
        """Stop queue workers"""
        self._running = False
        for worker in self._workers:
            worker.cancel()
        await asyncio.gather(*self._workers, return_exceptions=True)

    async def _worker(self, name: str):
        """Worker process that pulls from queue"""
        while self._running:
            try:
                job_id = await self.queue.get()

                job = self.jobs.get(job_id)
                if not job:
                    continue

                if job.cancel_requested:
                    job.status = JobStatus.CANCELLED
                    job.completed_at = datetime.utcnow()
                    continue

                # Process the job
                await self._process_job(job)

            except Exception as e:
                if job_id in self.jobs:
                    job = self.jobs[job_id]
                    job.status = JobStatus.FAILED
                    job.error = str(e)
                    job.completed_at = datetime.utcnow()

            finally:
                self.queue.task_done()
                self.active_tasks.discard(job_id)

    async def _process_job(self, job: Job):
        """Execute a single render job"""
        job.status = JobStatus.IN_PROGRESS
        job.started_at = datetime.utcnow()
        self.active_tasks.add(job.id)

        # Progress callback
        async def on_progress(data: dict):
            job.progress = data.get('progress', 0.0)

        try:
            if job.type == "media":
                output_path = job.options.get('output_path') or \
                    storage.get_output_path(job.id, 'mp4')

                job.options['output_path'] = output_path

                await self.renderer.render_media(job.options, on_progress)

                job.output_path = output_path
                job.output_url = storage.get_url(output_path)

            elif job.type == "still":
                output_path = job.options.get('output_path') or \
                    storage.get_output_path(job.id, 'png')

                job.options['output_path'] = output_path

                await self.renderer.render_still(job.options, on_progress)

                job.output_path = output_path
                job.output_url = storage.get_url(output_path)

            job.status = JobStatus.COMPLETED
            job.progress = 1.0

        except Exception as e:
            job.status = JobStatus.FAILED
            job.error = str(e)
            raise

        finally:
            job.completed_at = datetime.utcnow()

    async def enqueue(self, job_type: str, options: dict) -> str:
        """Add a new job to the queue"""
        job_id = str(uuid.uuid4())

        job = Job(
            id=job_id,
            type=job_type,
            options=options
        )

        self.jobs[job_id] = job
        await self.queue.put(job_id)

        return job_id

    async def cancel(self, job_id: str) -> bool:
        """Cancel a job"""
        job = self.jobs.get(job_id)
        if not job:
            return False

        if job.status == JobStatus.QUEUED:
            job.status = JobStatus.CANCELLED
            job.completed_at = datetime.utcnow()
            return True
        elif job.status == JobStatus.IN_PROGRESS:
            job.cancel_requested = True
            return True

        return False

    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID"""
        return self.jobs.get(job_id)

    def list_jobs(
        self,
        status: Optional[JobStatus] = None,
        limit: int = 100,
        offset: int = 0
    ) -> tuple[List[Job], int]:
        """List all jobs, optionally filtered by status"""
        jobs = list(self.jobs.values())

        if status:
            jobs = [j for j in jobs if j.status == status]

        jobs.sort(key=lambda j: j.created_at, reverse=True)

        return jobs[offset:offset+limit], len(jobs)


# Global queue instance (will be initialized in main.py)
queue: Optional[RenderQueue] = None
