FROM python:3.11-slim

# Set labels for image metadata
LABEL org.opencontainers.image.title="To-Do List App"
LABEL org.opencontainers.image.description="A Flask-based REST API for managing tasks with comprehensive testing and CI/CD"
LABEL org.opencontainers.image.source="https://github.com/igiclarisse10-max/devops_cat"
LABEL org.opencontainers.image.vendor="Clarisse"

# Read version from build arg
ARG VERSION=1.0.0
ENV APP_VERSION=${VERSION}

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5000/')" || exit 1

EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
