# AgentForge-Web

A modern web interface for [AgentForge](https://github.com/gerimantas/AgentForge) AI agents, built with FastAPI and React.

## 🚀 Project Overview

AgentForge-Web provides a user-friendly web interface for interacting with AgentForge's powerful AI agent system. It combines the robust AI capabilities of AgentForge with a modern, responsive web application built on proven technologies.

### Key Features

- 🤖 **AI Agent Integration**: Execute AgentForge workflows through a web interface
- ⚡ **Real-time Updates**: Live progress tracking during agent execution
- 🔐 **Secure Authentication**: JWT-based user authentication system
- 📊 **Session Management**: Track and manage execution history
- 🎨 **Modern UI**: Responsive React interface with Tailwind CSS
- 🐳 **Docker Ready**: Containerized for easy deployment

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Client  │◄──►│  FastAPI Server │◄──►│   PostgreSQL    │
│                 │    │                 │    │                 │
│  - AgentChat    │    │  - Agent API    │    │  - Users        │
│  - AgentStatus  │    │  - Auth API     │    │  - Sessions     │
│  - Real-time UI │    │  - SSE Stream   │    │  - Results      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   AgentForge    │
                       │                 │
                       │  - Execution    │
                       │  - Maintenance  │
                       │  - Knowledge    │
                       └─────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Primary database
- **JWT** - Authentication
- **Server-Sent Events** - Real-time communication

### Frontend
- **React 18+** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Custom Hooks** - State management

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Orchestration
- **GitHub Actions** - CI/CD


## 📖 Documentation

Comprehensive project documentation is available in the [`project-docs/`](./project-docs/) directory:

- **[Action Plan](./project-docs/action-plan.md)** - Complete development roadmap
- **[Progress Tracker](./project-docs/progress-tracker.md)** - Live project progress
- **[Quick Checklist](./project-docs/checklist.md)** - Daily development tasks
- **[Technical Specs](./project-docs/technical-specs.md)** - Architecture and API details

## 🚀 Quick Start

> **Note**: This project is currently in the planning phase. Implementation will begin according to the action plan.

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15

### Development Setup (Planned)

```bash
# Clone repository
git clone https://github.com/gerimantas/agentforge-web.git
cd agentforge-web

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Backend will be available at http://localhost:8000
# Frontend will be available at http://localhost:3000
```

## 🤝 Contributing


## 📝 Related Projects

- **[AgentForge](https://github.com/gerimantas/AgentForge)** - Core AI agent system
- **[fullstack-fastapi-starter](https://github.com/gerimantas/fullstack-fastapi-starter)** - Base template reference

## 📄 License

This project will be licensed under the MIT License (to be added).

## 🔗 Links

- **Documentation**: [project-docs/](./project-docs/)
- **Issues**: [GitHub Issues](https://github.com/gerimantas/agentforge-web/issues)
- **Project Board**: [GitHub Projects](https://github.com/gerimantas/agentforge-web/projects)

---

**Project Start**: July 14, 2025  
**Status**: 📋 Planning Phase Complete  
**Next**: 🚀 Begin Implementation
