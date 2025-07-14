/**
 * API service for AgentForge-Web
 * 
 * Handles all HTTP communications with the backend API
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

class ApiService {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
    this.token = localStorage.getItem('access_token');
  }

  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`;
    }

    return headers;
  }

  setToken(token: string | null) {
    this.token = token;
    if (token) {
      localStorage.setItem('access_token', token);
    } else {
      localStorage.removeItem('access_token');
    }
  }

  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'GET',
        headers: this.getHeaders(),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      return { error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  async post<T>(endpoint: string, body?: any): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: body ? JSON.stringify(body) : undefined,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      return { error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  // Health check
  async healthCheck() {
    return this.get('/api/health');
  }

  // Authentication endpoints
  async login(email: string, password: string) {
    return this.post('/api/auth/login', { email, password });
  }

  async register(email: string, password: string) {
    return this.post('/api/auth/register', { email, password });
  }

  async getCurrentUser() {
    return this.get('/api/auth/me');
  }

  // Agent endpoints
  async getAgentSessions(skip: number = 0, limit: number = 20) {
    return this.get(`/api/agents/sessions?skip=${skip}&limit=${limit}`);
  }

  // Agent execution - returns session ID for streaming
  async executeAgent(request: { query: string; workflow_type: string }): Promise<ApiResponse<{ session_id: number; status: string; message: string }>> {
    return this.post('/api/agents/execute', request);
  }

  // Server-Sent Events for agent execution streaming
  createAgentExecutionStream(sessionId: number): EventSource {
    // For development, since backend uses mock auth, we can connect directly
    // TODO: In production, implement proper token passing for SSE
    const url = `${this.baseUrl}/api/agents/execute/${sessionId}/stream`;
    
    const eventSource = new EventSource(url);
    return eventSource;
  }
}

export const apiService = new ApiService();
export default apiService;
