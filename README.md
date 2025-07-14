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

## 📋 Project Status

**Current Phase**: Planning & Documentation  
**Progress**: 0% (Documentation Complete)  
**Timeline**: 6 weeks development cycle  
**Start Date**: July 14, 2025  

### Development Phases

1. **Phase 1**: Foundation & MVP (Weeks 1-3)
   - Project setup and backend foundation
   - AgentForge integration
   - Basic React frontend
   - Docker configuration

2. **Phase 2**: Enhanced Features (Weeks 4-5)
   - Authentication system
   - Session management
   - Error handling
   - Basic monitoring

3. **Phase 3**: Production Ready (Week 6)
   - Production configuration
   - CI/CD pipeline
   - Documentation & testing

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

This project follows a structured development approach:

1. **Check Documentation**: Review the [action plan](./project-docs/action-plan.md)
2. **Track Progress**: Use the [progress tracker](./project-docs/progress-tracker.md)
3. **Follow Checklist**: Reference the [daily checklist](./project-docs/checklist.md)
4. **Technical Details**: Consult [technical specifications](./project-docs/technical-specs.md)

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
