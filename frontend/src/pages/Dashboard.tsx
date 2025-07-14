/**
 * Dashboard page - main application interface
 */

import React from 'react';
import { Layout } from '../components/Layout';
import { AgentChat } from '../components/AgentChat';

export const Dashboard: React.FC = () => {
  return (
    <Layout>
      <div className="space-y-6">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome to AgentForge Web
          </h1>
          <p className="mt-2 text-lg text-gray-600">
            Interact with AI agents to optimize your queries and automate tasks
          </p>
        </div>
        
        <AgentChat />
        
        {/* TODO: Add session history component */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">
            Recent Sessions
          </h2>
          <p className="text-gray-500 text-center py-8">
            Session history will be displayed here once implemented
          </p>
        </div>
      </div>
    </Layout>
  );
};
