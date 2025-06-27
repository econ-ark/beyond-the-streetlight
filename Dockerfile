# Beyond the Streetlight - Reproducible Research Environment
# This Dockerfile creates a containerized environment for running the economic analysis

FROM python:3.9-slim

# Set metadata
LABEL maintainer="Econ-ARK Team"
LABEL description="Beyond the Streetlight: Economic Forecasting Analysis"
LABEL version="1.0.5"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.6.1

# Configure Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Copy application code (needed for Poetry to find local packages)
COPY . .

# Install dependencies
RUN poetry install --only main && rm -rf $POETRY_CACHE_DIR

# Make scripts executable
RUN chmod +x reproduce.sh run_analysis.sh install.sh

# Create output directories
RUN mkdir -p results figures data/output

# Set environment variables for reproducibility
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

# Default command runs the full reproduction
CMD ["poetry", "run", "./reproduce.sh"]

# Alternative commands for different use cases:
# - Development: docker run -it beyond-the-streetlight bash
# - Analysis only: docker run beyond-the-streetlight poetry run ./run_analysis.sh
# - Interactive: docker run -it -p 8888:8888 beyond-the-streetlight poetry run jupyter lab --ip=0.0.0.0 --allow-root 