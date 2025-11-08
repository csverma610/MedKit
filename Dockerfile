# Multi-stage build for MedKit

# Builder stage
FROM python:3.11-slim as builder

WORKDIR /tmp

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Build wheel files
RUN pip install --user --no-cache-dir wheel && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /tmp/wheels -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /tmp/wheels /tmp/wheels
COPY --from=builder /tmp/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache /tmp/wheels/* && \
    rm -rf /tmp/wheels

# Copy application
COPY . .

# Install MedKit in production mode
RUN pip install --no-cache-dir -e .

# Create non-root user
RUN useradd -m -u 1000 medkit && \
    chown -R medkit:medkit /app

USER medkit

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from medkit.core.config import Config; print('OK')" || exit 1

# Default command
ENTRYPOINT ["medkit"]
CMD ["--help"]
