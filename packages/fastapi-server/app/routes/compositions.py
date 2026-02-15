"""Composition-related endpoints"""
from fastapi import APIRouter, HTTPException, status
from ..models.composition import GetCompositionsRequest, GetCompositionsResponse
from ..services.renderer import NodeRenderer

router = APIRouter()
renderer = NodeRenderer()


@router.post("/compositions", response_model=GetCompositionsResponse)
async def get_compositions(request: GetCompositionsRequest):
    """Get available compositions from a Remotion bundle"""
    try:
        options = request.model_dump(exclude_none=True)
        comps = await renderer.get_compositions(options)

        # Map durationInFrames to duration_in_frames (Python naming)
        mapped_comps = []
        for comp in comps:
            mapped_comps.append({
                "id": comp.get("id"),
                "width": comp.get("width"),
                "height": comp.get("height"),
                "fps": comp.get("fps"),
                "duration_in_frames": comp.get("durationInFrames"),
                "default_output": comp.get("defaultOutput")
            })

        return GetCompositionsResponse(
            compositions=mapped_comps,
            serve_url=request.serve_url
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
