"""Render-related data models"""
from pydantic import BaseModel, Field, ConfigDict
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
    model_config = ConfigDict(populate_by_name=True)

    ignore_certificate_errors: Optional[bool] = Field(default=None, serialization_alias="ignoreCertificateErrors", validation_alias="ignore_certificate_errors")
    disable_web_security: Optional[bool] = Field(default=None, serialization_alias="disableWebSecurity", validation_alias="disable_web_security")
    gl: Optional[str] = None
    headless: Optional[bool] = None
    user_agent: Optional[str] = Field(default=None, serialization_alias="userAgent", validation_alias="user_agent")


class RenderMediaRequest(BaseModel):
    """Request to render a video"""
    model_config = ConfigDict(populate_by_name=True)

    serve_url: str = Field(..., description="URL to the Remotion bundle", serialization_alias="serveUrl", validation_alias="serve_url")
    composition: str = Field(..., description="Composition ID to render")
    input_props: Optional[Dict[str, Any]] = Field(default={}, description="Props to pass to composition", serialization_alias="inputProps", validation_alias="input_props")
    output_path: Optional[str] = Field(default=None, description="Output file path", serialization_alias="outputPath", validation_alias="output_path")
    codec: VideoCodec = Field(default=VideoCodec.H264, description="Video codec (default: h264 for mp4 compatibility)")
    chromium_options: Optional[ChromiumOptions] = Field(default=None, description="Browser options", serialization_alias="chromiumOptions", validation_alias="chromium_options")
    image_format: ValidStillImageFormats = Field(default=ValidStillImageFormats.JPEG, description="Frame format", serialization_alias="imageFormat", validation_alias="image_format")
    jpeg_quality: int = Field(default=80, ge=1, le=100, description="JPEG quality (1-100)", serialization_alias="jpegQuality", validation_alias="jpeg_quality")
    scale: int = Field(default=1, ge=1, le=10, description="Scale factor")
    every_nth_frame: int = Field(default=1, ge=1, description="Render every Nth frame", serialization_alias="everyNthFrame", validation_alias="every_nth_frame")
    frame_range: Optional[str] = Field(default=None, description="Frame range (e.g., '0-100')", serialization_alias="frameRange", validation_alias="frame_range")
    env_variables: Optional[Dict[str, str]] = Field(default=None, description="Environment variables", serialization_alias="envVariables", validation_alias="env_variables")
    muted: bool = Field(default=False, description="Mute audio")
    overwrite: bool = Field(default=False, description="Overwrite existing output")
    audio_bitrate: Optional[int] = Field(default=None, description="Audio bitrate", serialization_alias="audioBitrate", validation_alias="audio_bitrate")
    video_bitrate: Optional[int] = Field(default=None, description="Video bitrate", serialization_alias="videoBitrate", validation_alias="video_bitrate")
    # Fast encoding options
    fps: Optional[int] = Field(default=None, ge=1, le=144, description="Output FPS (lower = faster)")
    enforce_audio_track: Optional[bool] = Field(default=None, description="Enforce audio track in output", serialization_alias="enforceAudioTrack", validation_alias="enforce_audio_track")
    ffmpeg_craneflag: Optional[list[str]] = Field(default=None, description="FFmpeg crane flags for optimization", serialization_alias="ffmpegCraneflag", validation_alias="ffmpeg_craneflag")


class RenderMediaResponse(BaseModel):
    """Response for render media request"""
    job_id: str
    status: str
    message: str


class RenderStillRequest(BaseModel):
    """Request to render a still image"""
    model_config = ConfigDict(populate_by_name=True)

    serve_url: str = Field(..., description="URL to the Remotion bundle", serialization_alias="serveUrl", validation_alias="serve_url")
    composition: str = Field(..., description="Composition ID to render")
    input_props: Optional[Dict[str, Any]] = Field(default={}, description="Props to pass to composition", serialization_alias="inputProps", validation_alias="input_props")
    output_path: Optional[str] = Field(default=None, description="Output file path", serialization_alias="outputPath", validation_alias="output_path")
    frame: int = Field(default=0, ge=0, description="Frame number to render")
    image_format: ValidStillImageFormats = Field(default=ValidStillImageFormats.JPEG, description="Image format", serialization_alias="imageFormat", validation_alias="image_format")
    jpeg_quality: int = Field(default=80, ge=1, le=100, description="JPEG quality (1-100)", serialization_alias="jpegQuality", validation_alias="jpeg_quality")
    scale: float = Field(default=1.0, ge=0.1, le=10.0, description="Scale factor")
    overwrite: bool = Field(default=False, description="Overwrite existing output")


class RenderStillResponse(BaseModel):
    """Response for render still request"""
    job_id: str
    status: str
    message: str
