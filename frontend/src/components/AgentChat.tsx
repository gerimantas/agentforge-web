/**
 * AgentChat component for interacting with AI agents
 */

import React, { useState } from 'react';
import { useAgent } from '../hooks/useAgent';
import { AgentStatus } from './AgentStatus';

export const AgentChat: React.FC = () => {
  const [query, setQuery] = useState('');
  const [workflowType, setWorkflowType] = useState<'execution' | 'maintenance'>('execution');
  const { 
    executeAgent, 
    isExecuting, 
    currentUpdate, 
    executionHistory, 
    error, 
    sessionId,
    clearHistory, 
    stopExecution 
  } = useAgent();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isExecuting) return;

    await executeAgent({
      query: query.trim(),
      workflow_type: workflowType,
    });
  };

  const handleClear = () => {
    setQuery('');
    clearHistory();
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4">
          <h2 className="text-2xl font-bold text-white">AI Agent Assistant</h2>
          <p className="text-blue-100 mt-1">
            Execute AgentForge workflows to optimize your queries and tasks
          </p>
        </div>

        {/* Form */}
        <div className="p-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Workflow Type
              </label>
              <select
                value={workflowType}
                onChange={(e) => setWorkflowType(e.target.value as 'execution' | 'maintenance')}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                disabled={isExecuting}
              >
                <option value="execution">Query Optimization</option>
                <option value="maintenance">Knowledge Base Maintenance</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Your Query
              </label>
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter your query here... (e.g., 'Help me write a professional email requesting a salary increase')"
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                rows={4}
                disabled={isExecuting}
                required
              />
            </div>

            <div className="flex space-x-3">
              <button
                type="submit"
                disabled={!query.trim() || isExecuting}
                className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isExecuting ? 'Processing...' : 'Execute Agent'}
              </button>
              
              {isExecuting && (
                <button
                  type="button"
                  onClick={stopExecution}
                  className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors"
                >
                  Stop
                </button>
              )}
              
              <button
                type="button"
                onClick={handleClear}
                disabled={isExecuting}
                className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Clear
              </button>
            </div>
            
            {/* Session Info */}
            {sessionId && (
              <div className="mt-2 text-sm text-gray-500">
                Session ID: {sessionId}
              </div>
            )}
          </form>

          {/* Error Display */}
          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
              <div className="flex">
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">Error</h3>
                  <div className="mt-2 text-sm text-red-700">
                    <p>{error}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Agent Status */}
          {(isExecuting || currentUpdate || executionHistory.length > 0) && (
            <div className="mt-6">
              <AgentStatus 
                currentUpdate={currentUpdate}
                executionHistory={executionHistory}
                isExecuting={isExecuting}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
