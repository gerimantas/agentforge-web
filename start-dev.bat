@echo off
REM AgentForge-Web Docker Startup Script for Windows

echo 🚀 Starting AgentForge-Web Development Environment...

REM Check if .env file exists
if not exist .env (
    echo 📋 Creating .env file from template...
    copy .env.example .env
    echo ✅ .env file created. Please edit it with your configuration.
)

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

echo 🔧 Building and starting services...

REM Start development environment
docker-compose -f docker-compose.dev.yml up --build

echo 🎉 AgentForge-Web is running!
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
echo Database: localhost:5432
pause
