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
            env={**{"NODE_PATH": os.environ.get("NODE_PATH", "/usr/local/lib/node_modules")}, **os.environ}
        )

        print(f"DEBUG: Process started with PID: {process.pid}", flush=True)

        # Write input to stdin
        stdin_json = json.dumps(input_data) + "\n"
        process.stdin.write(stdin_json.encode('utf-8'))
        process.stdin.close()

        # Read output line by line with timeout
        final_result = {}
        line_count = 0
        last_progress_time = asyncio.get_event_loop().time()
        timeout_seconds = 600  # 10 minutes timeout

        while True:
            try:
                # Wait for output with timeout
                line = await asyncio.wait_for(
                    process.stdout.readline(),
                    timeout=30.0  # 30 seconds timeout per line
                )
            except asyncio.TimeoutError:
                # Check if process is still running
                if process.returncode is not None:
                    break

                # Check if we've exceeded total timeout
                current_time = asyncio.get_event_loop().time()
                if current_time - last_progress_time > timeout_seconds:
                    print(f"DEBUG: Process timeout after {timeout_seconds}s with no progress", flush=True)
                    process.kill()
                    raise RuntimeError(f"Process timeout after {timeout_seconds} seconds")

                # Continue waiting
                continue

            if not line:
                print(f"DEBUG: EOF reached after {line_count} lines", flush=True)
                break

            line_count += 1
            line_str = line.decode('utf-8').strip()

            try:
                data = json.loads(line_str)

                if data.get('type') == 'progress':
                    last_progress_time = asyncio.get_event_loop().time()  # Update last activity
                    print(f"DEBUG: Received progress: {data.get('data')}", flush=True)
                    if on_progress:
                        await on_progress(data.get('data'))
                elif data.get('type') == 'complete':
                    print(f"DEBUG: Received complete signal", flush=True)
                    final_result = {'status': 'success'}
                elif data.get('type') == 'compositions':
                    print(f"DEBUG: Received compositions", flush=True)
                    final_result = data
                elif data.get('type') == 'error':
                    print(f"DEBUG: Received error: {data.get('message')}", flush=True)
                    raise RuntimeError(data.get('message'))
                elif data.get('type') == 'info':
                    last_progress_time = asyncio.get_event_loop().time()  # Update last activity
                    print(f"DEBUG: [info] {data.get('message')}", flush=True)

            except json.JSONDecodeError:
                print(f"DEBUG: Failed to parse JSON: {line_str[:100]}", flush=True)
                continue

        await process.wait()

        print(f"DEBUG: Process finished with return code: {process.returncode}", flush=True)

        if process.returncode != 0:
            stderr_output = await process.stderr.read()
            error_msg = stderr_output.decode('utf-8')
            print(f"DEBUG: Process stderr: {error_msg}", flush=True)
            raise RuntimeError(f"Node.js process failed: {error_msg}")

        return final_result
