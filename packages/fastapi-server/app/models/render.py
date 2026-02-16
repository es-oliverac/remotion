"""Render-related data models"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum


class ValidStillImageFormats(str, Enum):
    """Valid still image formats"""
    JPEG = "jpeg"
    PNG = "png"
    WEBP = "webp"
    PDF = "pdf"


class VideoCodec(str, Enum):
    """Supported video codecs"""
    H264 = "h264"
    H265 = "h265"
    VP8 = "vp8"
    VP9 = "vp9"
    PRORES = "prores"


class ChromiumOptions(BaseModel):
    """Options for Chromium browser"""
    ignore_certificate_errors: Optional[bool] = None
    disable_web_security: Optional[bool] = None
    gl: Optional[str] = None
    headless: Optional[bool] = None
    user_agent: Optional[str] = None


class RenderMediaRequest(BaseModel):
    """Request to render a video"""
    serve_url: str = Field(..., description="URL to the Remotion bundle")
    composition: str = Field(..., description="Composition ID to render")
    input_props: Optional[Dict[str, Any]] = Field(default={}, description="Props to pass to composition")
    output_path: Optional[str] = Field(default=None, description="Output file path")
    codec: VideoCodec = Field(default=VideoCodec.H264, description="Video codec (default: h264 for mp4 compatibility)")
    chromium_options: Optional[ChromiumOptions] = Field(default=None, description="Browser options")
    image_format: ValidStillImageFormats = Field(default=ValidStillImageFormats.JPEG, description="Frame format")
    jpeg_quality: int = Field(default=80, ge=1, le=100, description="JPEG quality (1-100)")
    scale: int = Field(default=1, ge=1, le=10, description="Scale factor")
    every_nth_frame: int = Field(default=1, ge=1, description="Render every Nth frame")
    frame_range: Optional[str] = Field(default=None, description="Frame range (e.g., '0-100')")
    env_variables: Optional[Dict[str, str]] = Field(default=None, description="Environment variables")
    muted: bool = Field(default=False, description="Mute audio")
    overwrite: bool = Field(default=False, description="Overwrite existing output")
    audio_bitrate: Optional[int] = Field(default=None, description="Audio bitrate")
    video_bitrate: Optional[int] = Field(default=None, description="Video bitrate")
    # Fast encoding options
    fps: Optional[int] = Field(default=None, ge=1, le=144, description="Output FPS (lower = faster)")
    enforce_audio_track: Optional[bool] = Field(default=None, description="Enforce audio track in output")
    ffmpeg_craneflag: Optional[list[str]] = Field(default=None, description="FFmpeg crane flags for optimization")


class RenderMediaResponse(BaseModel):
    """Response for render media request"""
    job_id: str
    status: str
    message: str


class RenderStillRequest(BaseModel):
    """Request to render a still image"""
    serve_url: str = Field(..., description="URL to the Remotion bundle")
    composition: str = Field(..., description="Composition ID to render")
    input_props: Optional[Dict[str, Any]] = Field(default={}, description="Props to pass to composition")
    output_path: Optional[str] = Field(default=None, description="Output file path")
    frame: int = Field(default=0, ge=0, description="Frame number to render")
    image_format: ValidStillImageFormats = Field(default=ValidStillImageFormats.JPEG, description="Image format")
    jpeg_quality: int = Field(default=80, ge=1, le=100, description="JPEG quality (1-100)")
    scale: float = Field(default=1.0, ge=0.1, le=10.0, description="Scale factor")
    overwrite: bool = Field(default=False, description="Overwrite existing output")


class RenderStillResponse(BaseModel):
    """Response for render still request"""
    job_id: str
    status: str
    message: str
