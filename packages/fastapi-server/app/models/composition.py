"""Composition-related data models"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Composition(BaseModel):
    """Represents a Remotion composition"""
    id: str
    width: int
    height: int
    fps: int
    duration_in_frames: int
    default_output: Optional[Dict[str, Any]] = None


class GetCompositionsRequest(BaseModel):
    """Request to get available compositions"""
    serve_url: str = Field(..., description="URL to the Remotion bundle")
    input_props: Optional[Dict[str, Any]] = Field(default=None, description="Input props to pass")
    env_variables: Optional[Dict[str, str]] = Field(default=None, description="Environment variables")


class GetCompositionsResponse(BaseModel):
    """Response with list of compositions"""
    compositions: list[Composition]
    serve_url: str
