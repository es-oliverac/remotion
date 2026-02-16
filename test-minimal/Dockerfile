FROM node:22-bookworm-slim

WORKDIR /app

# Install Chrome dependencies and Python for serving
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
  && rm -rf /var/lib/apt/lists/*

# Install project dependencies
COPY package*.json ./
RUN npm install

# Install Chrome
RUN npx remotion browser ensure

# Copy source files
COPY src ./src
COPY remotion.config.* ./
COPY tsconfig.json ./

# Expose port
EXPOSE 3000

# Health check - verify Remotion studio is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:3000 || exit 1

# Run Remotion Studio (full editor with timeline)
# This serves both the visual editor AND exposes window.getStaticCompositions for the API
CMD ["npm", "start"]
