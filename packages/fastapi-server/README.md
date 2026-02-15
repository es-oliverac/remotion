# Remotion FastAPI Server

FastAPI-based HTTP wrapper for Remotion video rendering, optimized for n8n integration and easypanel deployment.

## Features

- Simple REST API for video and still rendering
- WebSocket support for real-time progress updates
- Async job queue with configurable concurrency
- Browser pool for performance optimization
- Docker-ready with easypanel configuration
- n8n integration examples
- Comprehensive API documentation with OpenAPI/Swagger

## Quick Start

### Docker

```bash
docker run -p 8000:8000 remotion/fastapi-server
```

### From Source

```bash
# Install dependencies
pip install -r requirements.txt

# Build Node.js wrapper
cd node && bun install && bun run build

# Run development server
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Examples

See [examples/](examples/) for n8n workflows and curl examples.

## License

SEE LICENSE IN LICENSE.md
