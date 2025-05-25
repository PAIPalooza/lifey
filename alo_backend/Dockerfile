FROM python:3.9-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Comment about required environment variables
# These should be set in the deployment environment, not in the Dockerfile
# Required: DATABASE_URL, SECRET_KEY

# Set a non-sensitive placeholder that will be overridden in production
ENV DATABASE_URL="postgresql://postgres:postgres@localhost:5432/alo_db"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Make entry point scripts executable
RUN chmod +x wsgi.py run.py

# Command to run the application
# Use the wsgi.py entry point for production deployments
CMD ["python", "wsgi.py"]
