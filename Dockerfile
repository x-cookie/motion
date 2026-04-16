# Motion Server Dockerfile
# https://github.com/cookie-may/motion
#
# Build:
#   docker build -t motion-server .
#
# Run:
#   docker run -d -p 8000:8000 -v motion-data:/data motion-server

FROM python:3.13-slim-bookworm

WORKDIR /app

# Install packages from PyPI
RUN pip install --no-cache-dir motion-ui[server]

# Copy demo scripts
COPY scripts/demo_data.py scripts/demo_data.json ./scripts/

# Create non-root user and data directory
RUN useradd -m -u 1000 motion \
    && mkdir -p /data \
    && chown -R motion:motion /data /app

USER motion

# Expose API port
EXPOSE 8000

# Data persistence volume
VOLUME /data

# Health check using Python (no curl needed)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Environment variables
# SQLAlchemy requires sqlite:/// prefix for database URL
ENV MOTION_STORAGE_DATABASE_URL=sqlite:////data/tasks.db
# Terminal settings for proper CLI/TUI output rendering (Rich/Textual)
ENV TERM=xterm-256color
ENV COLORTERM=truecolor

# Start motion-server
ENTRYPOINT ["motion-server", "--host", "0.0.0.0", "--port", "8000"]
