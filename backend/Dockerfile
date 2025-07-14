# Backend Dockerfile for development
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Clone AgentForge repository for integration
RUN git clone https://github.com/DataBassGit/AgentForge.git /agentforge

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies (including AgentForge)
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install -e /agentforge

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Development command with hot reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
