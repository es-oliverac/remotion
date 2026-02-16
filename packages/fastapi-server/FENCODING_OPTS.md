# FFmpeg Encoding Optimization Guide

This guide explains how to optimize video encoding speed for the Remotion FastAPI server.

## The Problem

H.264 encoding is **slow** by default. A 5-second video at 1080p/30fps can take 2-5 minutes to encode.

## Solutions

### 1. Use ProRes Codec (Fastest)

ProRes encoding is **3-5x faster** than H.264, but produces larger files.

```bash
curl -X POST https://n8n-remotion.alzadl.easypanel.host/api/v1/render/media \
  -H "Content-Type: application/json" \
  -d '{
    "serve_url": "https://n8n-remotion2.alzadl.easypanel.host",
    "composition": "HelloWorld",
    "output_path": "/app/outputs/test-prores.mov",
    "codec": "prores"
  }'
```

**Trade-offs:**
- ✅ **3-5x faster** encoding
- ✅ Better quality (less compression artifacts)
- ❌ **2-3x larger** file size
- ❌ `.mov` format (less compatible than MP4)

### 2. Reduce FPS

Reduce output framerate from 30fps to 24fps (20% faster).

```bash
curl -X POST https://n8n-remotion.alzadl.easypanel.host/api/v1/render/media \
  -H "Content-Type: application/json" \
  -d '{
    "serve_url": "https://n8n-remotion2.alzadl.easypanel.host",
    "composition": "HelloWorld",
    "output_path": "/app/outputs/test-24fps.mp4",
    "codec": "h264",
    "fps": 24
  }'
```

**Trade-offs:**
- ✅ 20% faster rendering
- ✅ 20% smaller file size
- ⚠️ Slightly less smooth motion

### 3. Use FFmpeg Ultrafast Preset

Pass the `-preset ultrafast` flag to FFmpeg for H.264.

```bash
curl -X POST https://n8n-remotion.alzadl.easypanel.host/api/v1/render/media \
  -H "Content-Type: application/json" \
  -d '{
    "serve_url": "https://n8n-remotion2.alzadl.easypanel.host",
    "composition": "HelloWorld",
    "output_path": "/app/outputs/test-ultrafast.mp4",
    "codec": "h264",
    "ffmpegCraneflag": ["-preset", "ultrafast"]
  }'
```

**Trade-offs:**
- ✅ **2-3x faster** than default H.264
- ❌ Lower quality per bitrate
- ❌ Slightly larger files

### 4. Combine Multiple Optimizations

For maximum speed:

```bash
curl -X POST https://n8n-remotion.alzadl.easypanel.host/api/v1/render/media \
  -H "Content-Type: application/json" \
  -d '{
    "serve_url": "https://n8n-remotion2.alzadl.easypanel.host",
    "composition": "HelloWorld",
    "output_path": "/app/outputs/test-fast.mp4",
    "codec": "prores",
    "fps": 24
  }'
```

This combines ProRes (fast codec) + 24fps (fewer frames).

## Codec Comparison

| Codec | Speed | File Size | Quality | Compatibility |
|-------|-------|-----------|---------|----------------|
| **prores** | ⚡⚡⚡ Fastest | 🔴🔴🔴 Large | 🟢 Perfect | 🟡 Medium (.mov) |
| **h264 + ultrafast** | ⚡⚡ Fast | 🟡 Medium | 🟡 Good | 🟢 Excellent (.mp4) |
| **h264 (default)** | ⚡ Slow | 🟢 Small | 🟢 Good | 🟢 Excellent (.mp4) |
| **h265** | 🔴 Very Slow | 🟢🟢 Smallest | 🟢 Perfect | 🟡 Medium |

## When to Use Each

### Use ProRes when:
- ✅ Encoding speed is critical
- ✅ Storage is not a concern
- ✅ Quality is more important than file size
- ✅ You plan to transcode to H.264 later

### Use H.264 + Ultrafast when:
- ✅ You need MP4 format
- ✅ Speed is important but quality matters
- ✅ File size should be reasonable

### Use H.264 Default when:
- ✅ Quality is most important
- ✅ File size must be small
- ⏱️ You can wait longer for encoding

## FFmpeg Crane Flags Reference

You can pass any FFmpeg flag using `ffmpegCraneflag`:

```bash
# Set preset (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)
"ffmpegCraneflag": ["-preset", "ultrafast"]

# Set CRF (lower = better quality, larger file)
"ffmpegCraneflag": ["-crf", "23"]

# Set bitrate
"ffmpegCraneflag": ["-b:v", "5M"]

# Combine multiple flags
"ffmpegCraneflag": ["-preset", "ultrafast", "-crf", "28"]
```

## Current Configuration

Your FastAPI server has these defaults:
- **Timeout**: 30 minutes (1800 seconds)
- **Per-line timeout**: 120 seconds
- **Resources**: 24GB RAM, 8 CPUs

These settings are optimized for slow encoding. You can monitor progress by checking the job status endpoint.

## Example: n8n Workflow

In n8n, use the HTTP Request node with:

```json
{
  "method": "POST",
  "url": "https://n8n-remotion.alzadl.easypanel.host/api/v1/render/media",
  "body": {
    "serve_url": "https://n8n-remotion2.alzadl.easypanel.host",
    "composition": "HelloWorld",
    "codec": "prores",
    "output_path": "/app/outputs/{{ $json.id }}.mov"
  }
}
```

Then poll the status endpoint:
```
GET /api/v1/jobs/{{ $json.job_id }}
```

Wait for `status: "completed"` before downloading.
