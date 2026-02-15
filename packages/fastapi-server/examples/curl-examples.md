# Remotion FastAPI Server - cURL Examples for n8n

## Base URL

Replace `http://localhost:8000` with your actual server URL.

## Health Check

```bash
curl http://localhost:8000/api/v1/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

## Render Video

### Basic Render

```bash
curl -X POST http://localhost:8000/api/v1/render/media \
  -H "Content-Type: application/json" \
  -d '{
    "serve_url": "https://remotion-assets.com/bundle.zip",
    "composition": "MyVideo",
    "input_props": {
      "title": "Hello World",
      "subtitle": "Generated with n8n"
    },
    "codec": "h264",
    "jpeg_quality": 80
  }'
```

Response:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "message": "Render job queued successfully"
}
```

### Render with Custom Output Path

```bash
curl -X POST http://localhost:8000/api/v1/render/media \
  -H "Content-Type: application/json" \
  -d '{
    "serve_url": "https://remotion-assets.com/bundle.zip",
    "composition": "MyVideo",
    "input_props": {"title": "Custom Video"},
    "output_path": "/app/outputs/my-video.mp4",
    "codec": "h264"
  }'
```

### Render with Frame Range

```bash
curl -X POST http://localhost:8000/api/v1/render/media \
  -H "Content-Type: application/json" \
  -d '{
    "serve_url": "https://remotion-assets.com/bundle.zip",
    "composition": "MyVideo",
    "frame_range": "0-100",
    "every_nth_frame": 2
  }'
```

### Muted Video

```bash
curl -X POST http://localhost:8000/api/v1/render/media \
  -H "Content-Type: application/json" \
  -d '{
    "serve_url": "https://remotion-assets.com/bundle.zip",
    "composition": "MyVideo",
    "muted": true
  }'
```

## Render Still Image

```bash
curl -X POST http://localhost:8000/api/v1/render/still \
  -H "Content-Type: application/json" \
  -d '{
    "serve_url": "https://remotion-assets.com/bundle.zip",
    "composition": "Thumbnail",
    "input_props": {
      "text": "Custom Thumbnail"
    },
    "image_format": "png",
    "frame": 0,
    "scale": 2.0
  }'
```

Response:
```json
{
  "job_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "queued",
  "message": "Still render job queued successfully"
}
```

## Get Compositions

```bash
curl -X POST http://localhost:8000/api/v1/compositions \
  -H "Content-Type: application/json" \
  -d '{
    "serve_url": "https://remotion-assets.com/bundle.zip"
  }'
```

Response:
```json
{
  "compositions": [
    {
      "id": "MyVideo",
      "width": 1920,
      "height": 1080,
      "fps": 30,
      "duration_in_frames": 900,
      "default_output": null
    },
    {
      "id": "Thumbnail",
      "width": 1920,
      "height": 1080,
      "fps": 30,
      "duration_in_frames": 30,
      "default_output": null
    }
  ],
  "serve_url": "https://remotion-assets.com/bundle.zip"
}
```

## Check Job Status

```bash
curl http://localhost:8000/api/v1/jobs/550e8400-e29b-41d4-a716-446655440000
```

Response (in progress):
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "in-progress",
  "progress": 0.45,
  "created_at": "2024-01-15T10:30:00",
  "started_at": "2024-01-15T10:30:01",
  "completed_at": null,
  "output_url": null,
  "output_path": "/app/outputs/550e8400-e29b-41d4-a716-446655440000.mp4",
  "error": null
}
```

Response (completed):
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 1.0,
  "created_at": "2024-01-15T10:30:00",
  "started_at": "2024-01-15T10:30:01",
  "completed_at": "2024-01-15T10:32:30",
  "output_url": "http://localhost:8000/outputs/550e8400-e29b-41d4-a716-446655440000.mp4",
  "output_path": "/app/outputs/550e8400-e29b-41d4-a716-446655440000.mp4",
  "error": null
}
```

## Cancel Job

```bash
curl -X DELETE http://localhost:8000/api/v1/jobs/550e8400-e29b-41d4-a716-446655440000
```

Response:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "cancelled",
  "message": "Job cancelled successfully"
}
```

## List Jobs

### All Jobs
```bash
curl http://localhost:8000/api/v1/jobs
```

### Filter by Status
```bash
curl "http://localhost:8000/api/v1/jobs?status=in-progress"
```

### Pagination
```bash
curl "http://localhost:8000/api/v1/jobs?limit=10&offset=20"
```

Response:
```json
{
  "jobs": [
    {
      "job_id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "completed",
      "progress": 1.0,
      "created_at": "2024-01-15T10:30:00",
      "started_at": "2024-01-15T10:30:01",
      "completed_at": "2024-01-15T10:32:30",
      "output_url": "http://localhost:8000/outputs/550e8400-e29b-41d4-a716-446655440000.mp4",
      "output_path": "/app/outputs/550e8400-e29b-41d4-a716-446655440000.mp4",
      "error": null
    }
  ],
  "total": 25,
  "limit": 10,
  "offset": 20
}
```

## Download Output

Once a job is completed, download the output file:

```bash
curl -O http://localhost:8000/outputs/550e8400-e29b-41d4-a716-446655440000.mp4
```

## n8n Workflow Example

### Step 1: Render Video

Use the **HTTP Request** node in n8n:

- **Method**: POST
- **URL**: `http://your-server:8000/api/v1/render/media`
- **Authentication**: None
- **Body Parameters** (JSON):
  ```json
  {
    "serve_url": "https://remotion-assets.com/bundle.zip",
    "composition": "MyVideo",
    "input_props": {
      "title": "={{ $json.title }}",
      "subtitle": "={{ $json.description }}"
    }
  }
  ```

### Step 2: Wait for Completion

Use the **Wait** node:
- **Amount**: 5 seconds

### Step 3: Check Status (Loop)

Use the **HTTP Request** node:
- **Method**: GET
- **URL**: `=http://your-server:8000/api/v1/jobs/{{ $node["Render Video"].json["job_id"] }}`

Add a condition to check if status is "completed". If not, loop back to Step 2.

### Step 4: Download Video

Use the **HTTP Request** node:
- **Method**: GET
- **Response Format**: File
- **URL**: `={{ $node["Check Status"].json["output_url"] }}`
