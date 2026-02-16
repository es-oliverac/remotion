FROM node:22-bookworm-slim

WORKDIR /app

# Install Chrome dependencies, Python, and fonts for rendering
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
  libpango-1.0-0 \
  libcairo2 \
  libcups2 \
  curl \
  python3 \
  python3-pip \
  fonts-liberation \
  fonts-noto-color-emoji \
  fonts-dejavu-core \
  fonts-dejavu \
  fontconfig \
  && rm -rf /var/lib/apt/lists/* \
  && fc-cache -fv

# Install project dependencies
COPY package*.json ./
RUN npm install

# Install Chrome
RUN npx remotion browser ensure

# Copy source files
COPY src ./src
COPY remotion.config.* ./
COPY tsconfig.json ./

# Copy the custom server script
COPY serve.py /app/serve.py

# Build the Remotion bundle (exposes window.getStaticCompositions)
RUN npm run build

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:3000/index.html || exit 1

# Serve the bundle with custom SPA server
WORKDIR /app/build
CMD ["python3", "/app/serve.py"]
