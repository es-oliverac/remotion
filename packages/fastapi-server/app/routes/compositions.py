"""Composition-related endpoints"""
from fastapi import APIRouter, HTTPException, status
from ..models.composition import GetCompositionsRequest, GetCompositionsResponse
from ..services.renderer import NodeRenderer

router = APIRouter()
renderer = NodeRenderer()


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


@router.post("/compositions", response_model=GetCompositionsResponse)
async def get_compositions(request: GetCompositionsRequest):
    """Get available compositions from a Remotion bundle"""
    try:
        options = request.model_dump(exclude_none=True)

        # Ensure inputProps is an object, not None
        if "input_props" in options:
            if options["input_props"] is None:
                options["input_props"] = {}

        # Ensure envVariables is an object, not None
        if "env_variables" in options:
            if options["env_variables"] is None:
                options["env_variables"] = {}

        # Convert snake_case to camelCase for Node.js wrapper
        options = convert_dict_to_camel_case(options)

        # Debug log
        print(f"DEBUG: Options to Node.js: {options}", flush=True)

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
        import traceback
        print(f"ERROR: {str(e)}\n{traceback.format_exc()}", flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
