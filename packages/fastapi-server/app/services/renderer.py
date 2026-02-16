"""Node.js renderer subprocess wrapper"""
import json
import subprocess
import asyncio
import os
from typing import Optional, Dict, Any, Callable, Awaitable
from pathlib import Path
from ..config import settings


class NodeRenderer:
    """Wrapper for Node.js renderer process"""

    def __init__(self):
        # Go up from services/ to app/, then to node/
        base_path = Path(__file__).parent.parent.parent
        self.node_path = base_path / "node" / "renderer.ts"
        self.node_modules_path = base_path / "node" / "node_modules"
        if not self.node_path.exists():
            raise RuntimeError(f"Node renderer not found at {self.node_path}")

    async def render_media(
        self,
        options: Dict[str, Any],
        on_progress: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None
    ) -> Dict[str, Any]:
        """Execute renderMedia command in Node.js subprocess"""
        input_data = {
            "command": "renderMedia",
            "options": options
        }
        return await self._execute(input_data, on_progress)

    async def render_still(
        self,
        options: Dict[str, Any],
        on_progress: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None
    ) -> Dict[str, Any]:
        """Execute renderStill command in Node.js subprocess"""
        input_data = {
            "command": "renderStill",
            "options": options
        }
        return await self._execute(input_data, on_progress)

    async def get_compositions(
        self,
        options: Dict[str, Any]
    ) -> list[Dict[str, Any]]:
        """Execute getCompositions command in Node.js subprocess"""
        input_data = {
            "command": "getCompositions",
            "options": options
        }
        result = await self._execute(input_data, None)
        return result.get("data", [])

    async def _execute(
        self,
        input_data: Dict[str, Any],
        on_progress: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None
    ) -> Dict[str, Any]:
        """Execute Node.js process and handle output"""
        # Use tsx to run TypeScript directly
        tsx_path = self.node_modules_path / ".bin" / "tsx"

        # Debug logging
        print(f"DEBUG: Executing Node.js with input: {json.dumps(input_data, indent=2)}", flush=True)

        process = await asyncio.create_subprocess_exec(
            str(tsx_path),
            str(self.node_path),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(self.node_path.parent),
            env={**{"NODE_PATH": "/usr/local/lib/node_modules"}, **{"PATH": os.environ.get("PATH", "")}}
        )

        # Write input to stdin
        stdin_json = json.dumps(input_data) + "\n"
        process.stdin.write(stdin_json.encode('utf-8'))
        process.stdin.close()

        # Read output line by line
        final_result = {}

        while True:
            line = await process.stdout.readline()
            if not line:
                break

            try:
                data = json.loads(line.decode('utf-8').strip())

                if data.get('type') == 'progress':
                    if on_progress:
                        await on_progress(data.get('data'))
                elif data.get('type') == 'complete':
                    final_result = {'status': 'success'}
                elif data.get('type') == 'compositions':
                    final_result = data
                elif data.get('type') == 'error':
                    raise RuntimeError(data.get('message'))

            except json.JSONDecodeError:
                continue

        await process.wait()

        if process.returncode != 0:
            stderr_output = await process.stderr.read()
            error_msg = stderr_output.decode('utf-8')
            raise RuntimeError(f"Node.js process failed: {error_msg}")

        return final_result
