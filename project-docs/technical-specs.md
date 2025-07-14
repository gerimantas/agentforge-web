# AgentForge-Web Technical Specifications

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Client  │    │  FastAPI Server │    │   PostgreSQL    │
│                 │    │                 │    │                 │
│  - AgentChat    │◄──►│  - Agent API    │◄──►│  - Users        │
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

## Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT with passlib[bcrypt]
- **Async**: asyncio for concurrent operations
- **Streaming**: Server-Sent Events (SSE)
- **Validation**: Pydantic v2

### Frontend
- **Framework**: React 18+
- **Language**: TypeScript 5+
- **Build Tool**: Vite 5+
- **Styling**: Tailwind CSS 3+
- **State Management**: React hooks + Context
- **HTTP Client**: Fetch API with custom hooks
- **Real-time**: EventSource (SSE)

### DevOps
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Environment**: Development & Production configs
- **Monitoring**: Health checks + Basic metrics

## API Specification

### Authentication Endpoints

```typescript
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "securepassword"
}

POST /api/auth/login
{
  "email": "user@example.com", 
  "password": "securepassword"
}
→ { "access_token": "jwt_token", "token_type": "bearer" }
```

### Agent Endpoints

```typescript
POST /api/agents/execute
Headers: Authorization: Bearer <token>
Content-Type: text/event-stream
{
  "query": "Help me write a professional email",
  "workflow_type": "execution" | "maintenance"
}
→ SSE Stream:
data: {"type": "status", "status": "analyzing", "progress": 30}
data: {"type": "result", "status": "completed", "result": "..."}

GET /api/agents/sessions?skip=0&limit=20
Headers: Authorization: Bearer <token>
→ [
  {
    "id": 1,
    "query": "...",
    "status": "completed",
    "final_result": "...",
    "created_at": "2025-07-14T10:00:00Z"
  }
]
```

### Health & Monitoring

```typescript
GET /api/health
→ {"status": "healthy", "timestamp": "2025-07-14T10:00:00Z"}

GET /api/metrics
→ {
  "total_sessions": 150,
  "recent_sessions": 25,
  "timestamp": "2025-07-14T10:00:00Z"
}
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Agent Sessions Table
```sql
CREATE TABLE agent_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    query TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'queued',
    current_agent VARCHAR(100),
    progress INTEGER DEFAULT 0,
    intermediate_results JSONB DEFAULT '[]'::jsonb,
    final_result TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
```

## Frontend Component Hierarchy

```
App
├── AuthProvider
├── Router
    ├── LoginPage
    ├── Dashboard
        ├── Layout
        │   ├── Header
        │   ├── Navigation
        │   └── Footer
        ├── AgentChat
        │   ├── QueryForm
        │   ├── AgentStatus
        │   └── ResultDisplay
        └── SessionHistory
            ├── SessionList
            └── SessionDetail
```

## React Hooks Architecture

```typescript
// useAuth.ts - Authentication management
const useAuth = () => ({
  user: User | null,
  login: (email: string, password: string) => Promise<void>,
  logout: () => void,
  isAuthenticated: boolean,
  isLoading: boolean
});

// useAgent.ts - Agent execution management
const useAgent = () => ({
  executeAgent: (request: AgentRequest) => Promise<void>,
  isExecuting: boolean,
  currentUpdate: AgentUpdate | null,
  executionHistory: AgentUpdate[],
  error: string | null
});

// useSessionHistory.ts - Session management
const useSessionHistory = () => ({
  sessions: AgentSession[],
  loading: boolean,
  loadSessions: (skip?: number, limit?: number) => Promise<void>,
  exportSession: (sessionId: number) => Promise<void>
});
```

## Environment Configuration

### Development (.env.dev)
```bash
# Backend
DATABASE_URL=postgresql://postgres:postgres@db:5432/agentforge
SECRET_KEY=dev-secret-key-change-in-production
OPENAI_API_KEY=your-openai-api-key
SERPER_API_KEY=your-serper-api-key
MAX_AGENT_ITERATIONS=3
AGENT_TIMEOUT=300
ALLOWED_ORIGINS=["http://localhost:3000"]

# Frontend
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

### Production (.env.prod)
```bash
# Backend
DATABASE_URL=postgresql://user:password@prod-db:5432/agentforge
SECRET_KEY=super-secure-production-key
OPENAI_API_KEY=prod-openai-api-key
SERPER_API_KEY=prod-serper-api-key
MAX_AGENT_ITERATIONS=5
AGENT_TIMEOUT=600
ALLOWED_ORIGINS=["https://yourdomain.com"]

# Frontend
VITE_API_URL=https://api.yourdomain.com
VITE_WS_URL=wss://api.yourdomain.com
```

## Security Considerations

### Authentication
- JWT tokens with configurable expiration
- Password hashing using bcrypt
- Protected routes with middleware
- Token refresh mechanism

### Input Validation
- Pydantic models for API validation
- SQL injection prevention via ORM
- XSS prevention in frontend
- CORS configuration for API access

### AgentForge Integration
- Sandboxed execution environment
- Timeout mechanisms for long-running operations
- Resource usage monitoring
- Error isolation

## Performance Considerations

### Backend Optimization
- Async/await for I/O operations
- Connection pooling for database
- Caching for frequently accessed data
- Background tasks for heavy operations

### Frontend Optimization
- Code splitting with Vite
- Lazy loading of components
- Debounced search inputs
- Memoization of expensive computations

### Real-time Communication
- Server-Sent Events over WebSocket (simpler)
- Heartbeat mechanism for connection health
- Automatic reconnection on disconnect
- Efficient data serialization

## Testing Strategy

### Backend Testing
```bash
# Unit tests
pytest tests/unit/

# Integration tests  
pytest tests/integration/

# API tests
pytest tests/api/
```

### Frontend Testing
```bash
# Unit tests
npm test

# Component tests
npm run test:components

# E2E tests
npm run test:e2e
```

## Deployment Architecture

### Development
```yaml
# docker-compose.dev.yml
services:
  backend:
    build: ./backend
    volumes: ["./backend:/app"]
    ports: ["8000:8000"]
    
  frontend:
    build: ./frontend  
    volumes: ["./frontend:/app"]
    ports: ["3000:3000"]
    
  db:
    image: postgres:15
    ports: ["5432:5432"]
```

### Production
```yaml
# docker-compose.prod.yml
services:
  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile.prod
    restart: unless-stopped
    
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    restart: unless-stopped
    
  db:
    image: postgres:15
    restart: unless-stopped
    volumes: ["postgres_data:/var/lib/postgresql/data"]
    
  nginx:
    image: nginx:alpine
    ports: ["80:80", "443:443"]
```

## Monitoring & Logging

### Health Checks
- `/api/health` endpoint for service status
- Database connection verification
- AgentForge service availability
- Memory and CPU usage tracking

### Metrics Collection
- Request/response times
- Agent execution statistics
- User activity patterns
- Error rates and types

### Logging Strategy
- Structured logging with JSON format
- Different log levels (DEBUG, INFO, WARN, ERROR)
- Request tracing with correlation IDs
- Sensitive data filtering

---

**Version**: 1.0  
**Last Updated**: July 14, 2025  
**Next Review**: July 21, 2025
