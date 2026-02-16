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
            print("DEBUG: Queue workers already running", flush=True)
            return

        self._running = True
        print(f"DEBUG: Starting {self.max_concurrent} queue workers", flush=True)
        for i in range(self.max_concurrent):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self._workers.append(worker)
        print(f"DEBUG: {len(self._workers)} workers started", flush=True)

    async def stop(self):
        """Stop queue workers"""
        self._running = False
        for worker in self._workers:
            worker.cancel()
        await asyncio.gather(*self._workers, return_exceptions=True)

    async def _worker(self, name: str):
        """Worker process that pulls from queue"""
        print(f"DEBUG: Worker {name} started", flush=True)
        while self._running:
            try:
                print(f"DEBUG: Worker {name} waiting for job...", flush=True)
                job_id = await self.queue.get()
                print(f"DEBUG: Worker {name} got job {job_id}", flush=True)

                job = self.jobs.get(job_id)
                if not job:
                    print(f"DEBUG: Worker {name} - job {job_id} not found", flush=True)
                    continue

                if job.cancel_requested:
                    print(f"DEBUG: Worker {name} - job {job_id} was cancelled", flush=True)
                    job.status = JobStatus.CANCELLED
                    job.completed_at = datetime.utcnow()
                    continue

                # Process the job
                print(f"DEBUG: Worker {name} processing job {job_id}", flush=True)
                await self._process_job(job)
                print(f"DEBUG: Worker {name} finished job {job_id}", flush=True)

            except Exception as e:
                print(f"DEBUG: Worker {name} error: {str(e)}", flush=True)
                import traceback
                print(f"DEBUG: Traceback: {traceback.format_exc()}", flush=True)
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
        print(f"DEBUG: Processing job {job.id} (type: {job.type})", flush=True)
        print(f"DEBUG: Job options: {job.options}", flush=True)

        job.status = JobStatus.IN_PROGRESS
        job.started_at = datetime.utcnow()
        self.active_tasks.add(job.id)

        # Progress callback
        async def on_progress(data: dict):
            job.progress = data.get('progress', 0.0)
            print(f"DEBUG: Job {job.id} progress: {job.progress}", flush=True)

        try:
            if job.type == "media":
                output_path = job.options.get('output_path') or \
                    storage.get_output_path(job.id, 'mp4')

                job.options['output_path'] = output_path
                print(f"DEBUG: Rendering media to {output_path}", flush=True)

                await self.renderer.render_media(job.options, on_progress)

                job.output_path = output_path
                job.output_url = storage.get_url(output_path)
                print(f"DEBUG: Media rendered successfully to {output_path}", flush=True)

            elif job.type == "still":
                output_path = job.options.get('output_path') or \
                    storage.get_output_path(job.id, 'png')

                job.options['output_path'] = output_path
                print(f"DEBUG: Rendering still to {output_path}", flush=True)

                await self.renderer.render_still(job.options, on_progress)

                job.output_path = output_path
                job.output_url = storage.get_url(output_path)
                print(f"DEBUG: Still rendered successfully to {output_path}", flush=True)

            job.status = JobStatus.COMPLETED
            job.progress = 1.0
            print(f"DEBUG: Job {job.id} completed successfully", flush=True)

        except Exception as e:
            print(f"DEBUG: Job {job.id} failed: {str(e)}", flush=True)
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}", flush=True)
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
        print(f"DEBUG: Enqueueing job {job_id} (type: {job_type})", flush=True)
        await self.queue.put(job_id)
        print(f"DEBUG: Job {job_id} added to queue, queue size: {self.queue.qsize()}", flush=True)

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
