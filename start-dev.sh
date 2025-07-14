#!/bin/bash

# AgentForge-Web Docker Startup Script

echo "🚀 Starting AgentForge-Web Development Environment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your configuration."
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "🔧 Building and starting services..."

# Start development environment
docker-compose -f docker-compose.dev.yml up --build

echo "🎉 AgentForge-Web is running!"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo "Database: localhost:5432"
