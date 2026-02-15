# Multi-stage build for FastAPI + Node.js

# Stage 1: Prepare Node.js wrapper
FROM node:lts-bookworm-slim AS node-builder

WORKDIR /build

# Copy wrapper files
COPY node/package.json ./
COPY node/renderer.ts ./

# Install dependencies
RUN npm install

# Stage 2: Python runtime with Remotion
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install system dependencies for Chrome
RUN apt-get update && apt-get install -y \
  libnss3 \
  libdbus-1-3 \
  libatk1.0-0 \
  libgbm-dev \
  libasound2 \
  libxrandr2 \
  libxkbcommon-dev \
  libxfixes3 \
  libxcomposite1 \
  libxdamage1 \
  libatk-bridge2.0-0 \
  libcups2 \
  curl \
  gnupg \
  && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
  apt-get install -y nodejs && \
  rm -rf /var/lib/apt/lists/*

# Install Remotion and @remotion/renderer globally
RUN npm install -g remotion @remotion/renderer

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python application
COPY app ./app

# Copy Node.js wrapper dependencies and script
COPY --from=node-builder /build/node_modules ./node/node_modules
COPY --from=node-builder /build/package.json ./node/
COPY --from=node-builder /build/renderer.ts ./node/

# Create output directory
RUN mkdir -p /app/outputs

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV OUTPUT_DIR=/app/outputs
ENV NODE_PATH=/usr/local/lib/node_modules

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
