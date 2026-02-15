"""Storage management for output files"""
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
from ..config import settings


class StorageManager:
    """Manage output files and URLs"""

    def __init__(self):
        self.output_dir = Path(settings.OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.base_url = settings.BASE_URL.rstrip('/')

    def get_output_path(self, job_id: str, extension: str) -> str:
        """Generate output path for a job"""
        filename = f"{job_id}.{extension}"
        return str(self.output_dir / filename)

    def get_url(self, output_path: str) -> str:
        """Get public URL for output file"""
        filename = Path(output_path).name
        return f"{self.base_url}/outputs/{filename}"

    def ensure_output_dir(self):
        """Ensure output directory exists"""
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def cleanup_old_files(self, max_age_hours: int = 24):
        """Remove old output files"""
        cutoff = datetime.now() - timedelta(hours=max_age_hours)

        for file_path in self.output_dir.iterdir():
            if file_path.is_file():
                stat = file_path.stat()
                modified_time = datetime.fromtimestamp(stat.st_mtime)

                if modified_time < cutoff:
                    try:
                        file_path.unlink()
                    except Exception:
                        pass


# Global storage instance
storage = StorageManager()
