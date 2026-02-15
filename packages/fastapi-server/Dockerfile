# Multi-stage build for FastAPI + Node.js

# Stage 1: Build Node.js wrapper
FROM node:lts-bookworm-slim AS node-builder

# Install Chrome dependencies
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
  && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy package files
COPY node/package.json ./
COPY node/tsconfig.json ./
COPY node/renderer.ts ./

# Install dependencies and build
RUN npm install && npm run build

# Stage 2: Python runtime
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

# Install Remotion dependencies globally
RUN npm install -g remotion @remotion/renderer

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python application
COPY app ./app

# Copy built Node.js wrapper
COPY --from=node-builder /build/dist ./node/dist

# Create output directory
RUN mkdir -p /app/outputs

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV OUTPUT_DIR=/app/outputs

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
