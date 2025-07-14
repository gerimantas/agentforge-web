/**
 * Agent execution hook for managing agent workflows
 */

import { useState, useCallback, useRef } from 'react';
import { AgentRequest, AgentUpdate } from '../types/agent';
import apiService from '../services/api';

export const useAgent = () => {
  const [isExecuting, setIsExecuting] = useState(false);
  const [currentUpdate, setCurrentUpdate] = useState<AgentUpdate | null>(null);
  const [executionHistory, setExecutionHistory] = useState<AgentUpdate[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<number | null>(null);
  
  // Keep track of current EventSource for cleanup
  const eventSourceRef = useRef<EventSource | null>(null);

  const executeAgent = useCallback(async (request: AgentRequest) => {
    setIsExecuting(true);
    setError(null);
    setExecutionHistory([]);
    setCurrentUpdate(null);
    setSessionId(null);

    // Clean up any existing EventSource
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }

    try {
      // Step 1: Start the agent execution
      const response = await apiService.executeAgent(request);
      
      if (response.error) {
        throw new Error(response.error);
      }

      if (!response.data?.session_id) {
        throw new Error('No session ID returned from server');
      }

      const newSessionId = response.data.session_id;
      setSessionId(newSessionId);

      // Step 2: Connect to SSE stream for real-time updates
      const eventSource = apiService.createAgentExecutionStream(newSessionId);
      eventSourceRef.current = eventSource;

      eventSource.onmessage = (event) => {
        try {
          const update: AgentUpdate = JSON.parse(event.data);
          
          // Skip keepalive messages
          if (update.type === 'keepalive') {
            return;
          }

          // Add timestamp to update
          const updateWithTimestamp = {
            ...update,
            timestamp: new Date().toISOString()
          };

          setCurrentUpdate(updateWithTimestamp);
          setExecutionHistory(prev => [...prev, updateWithTimestamp]);

          // Check if execution is complete
          if (update.status === 'completed' || update.status === 'failed') {
            setIsExecuting(false);
            eventSource.close();
            eventSourceRef.current = null;
          }
        } catch (err) {
          console.error('Error parsing SSE message:', err);
          setError('Error parsing server response');
        }
      };

      eventSource.onerror = (error) => {
        console.error('SSE connection error:', error);
        setError('Connection to server lost. Please try again.');
        setIsExecuting(false);
        eventSource.close();
        eventSourceRef.current = null;
      };

      eventSource.onopen = () => {
        console.log('SSE connection established');
      };
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setIsExecuting(false);
    }
  }, []);

  const clearHistory = useCallback(() => {
    setExecutionHistory([]);
    setCurrentUpdate(null);
    setError(null);
    setSessionId(null);
    
    // Clean up EventSource
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
  }, []);

  const stopExecution = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    setIsExecuting(false);
  }, []);

  return {
    executeAgent,
    isExecuting,
    currentUpdate,
    executionHistory,
    error,
    sessionId,
    clearHistory,
    stopExecution,
  };
};
