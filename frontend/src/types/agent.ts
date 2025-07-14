/**
 * Agent type definitions for TypeScript
 */

export interface AgentRequest {
  query: string;
  workflow_type: 'execution' | 'maintenance';
}

export interface AgentExecuteResponse {
  session_id: number;
  status: string;
  message: string;
}

export interface AgentUpdate {
  type: 'status' | 'result' | 'error' | 'keepalive';
  status: 'queued' | 'analyzing' | 'executing' | 'completed' | 'failed';
  message: string;
  current_agent?: string;
  progress?: number;
  result?: string;
  final_result?: string;
  error?: string;
  error_message?: string;
  timestamp?: string;
}

export interface AgentSession {
  id: number;
  user_id: number;
  query: string;
  workflow_type: string;
  status: string;
  current_agent?: string;
  progress: number;
  intermediate_results: any[];
  final_result?: string;
  error_message?: string;
  created_at: string;
  started_at?: string;
  completed_at?: string;
}

export interface User {
  id: number;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
}
