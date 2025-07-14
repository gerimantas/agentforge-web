/**
 * AgentStatus component for displaying agent execution progress
 */

import React from 'react';
import { AgentUpdate } from '../types/agent';

interface AgentStatusProps {
  currentUpdate: AgentUpdate | null;
  executionHistory: AgentUpdate[];
  isExecuting: boolean;
}

export const AgentStatus: React.FC<AgentStatusProps> = ({
  currentUpdate,
  executionHistory,
  isExecuting,
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600';
      case 'failed': return 'text-red-600';
      case 'executing': return 'text-blue-600';
      case 'analyzing': return 'text-yellow-600';
      default: return 'text-gray-600';
    }
  };

  const getProgressBarColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-500';
      case 'failed': return 'bg-red-500';
      case 'executing': return 'bg-blue-500';
      case 'analyzing': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return '✅';
      case 'failed': return '❌';
      case 'executing': return '⚙️';
      case 'analyzing': return '🔍';
      default: return '⏳';
    }
  };

  return (
    <div className="space-y-4">
      {/* Current Status */}
      {currentUpdate && (
        <div className="border border-gray-200 rounded-lg p-4 bg-gray-50">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center space-x-2">
              <span className="text-lg">{getStatusIcon(currentUpdate.status)}</span>
              <span className={`font-medium text-sm uppercase tracking-wide ${getStatusColor(currentUpdate.status)}`}>
                {currentUpdate.status}
              </span>
            </div>
            {currentUpdate.current_agent && (
              <div className="text-sm text-gray-600 bg-white px-2 py-1 rounded">
                Agent: <span className="font-medium">{currentUpdate.current_agent}</span>
              </div>
            )}
          </div>

          {/* Progress Bar */}
          {currentUpdate.progress !== undefined && (
            <div className="mb-3">
              <div className="flex justify-between text-sm text-gray-600 mb-1">
                <span>Progress</span>
                <span>{currentUpdate.progress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className={`h-2 rounded-full transition-all duration-300 ${getProgressBarColor(currentUpdate.status)}`}
                  style={{ width: `${currentUpdate.progress}%` }}
                />
              </div>
            </div>
          )}

          {/* Status Message */}
          <p className="text-sm text-gray-700 mb-3">{currentUpdate.message}</p>

          {/* Result */}
          {(currentUpdate.result || currentUpdate.final_result) && (
            <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-md">
              <h4 className="font-medium text-green-800 mb-2 flex items-center">
                <span className="mr-2">🎉</span>
                Optimized Result:
              </h4>
              <div className="text-green-700 whitespace-pre-wrap bg-white p-3 rounded border">
                {currentUpdate.final_result || currentUpdate.result}
              </div>
            </div>
          )}

          {/* Error */}
          {(currentUpdate.error || currentUpdate.error_message) && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
              <h4 className="font-medium text-red-800 mb-2 flex items-center">
                <span className="mr-2">⚠️</span>
                Error:
              </h4>
              <div className="text-red-700 whitespace-pre-wrap bg-white p-3 rounded border">
                {currentUpdate.error_message || currentUpdate.error}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Execution History */}
      {executionHistory.length > 1 && (
        <div className="border border-gray-200 rounded-lg p-4">
          <h3 className="font-medium text-gray-800 mb-3 flex items-center">
            <span className="mr-2">📋</span>
            Execution Timeline
          </h3>
          <div className="space-y-2 max-h-60 overflow-y-auto">
            {executionHistory.map((update, index) => (
              <div 
                key={index} 
                className="flex items-center text-sm p-3 bg-gray-50 rounded border-l-4 border-gray-300"
                style={{
                  borderLeftColor: update.status === 'completed' ? '#10b981' : 
                                  update.status === 'failed' ? '#ef4444' : 
                                  update.status === 'executing' ? '#3b82f6' : '#f59e0b'
                }}
              >
                <span className="mr-2">{getStatusIcon(update.status)}</span>
                <div className="flex-1">
                  <span className={`font-medium ${getStatusColor(update.status)}`}>
                    {update.status}
                  </span>
                  {update.current_agent && (
                    <span className="ml-2 text-gray-600">
                      ({update.current_agent})
                    </span>
                  )}
                  <span className="ml-2 text-gray-700">
                    {update.message}
                  </span>
                </div>
                {update.progress !== undefined && (
                  <span className="text-xs text-gray-500 ml-2">
                    {update.progress}%
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Loading Indicator */}
      {isExecuting && (
        <div className="flex items-center justify-center text-blue-600">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
          <span className="text-sm">Agent is working...</span>
        </div>
      )}
    </div>
  );
};
