/**
 * Layout component providing the main application structure
 */

import React from 'react';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                AgentForge Web
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              {/* TODO: Add navigation and user menu */}
              <button className="text-gray-500 hover:text-gray-700">
                Settings
              </button>
              <button className="text-gray-500 hover:text-gray-700">
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-auto">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-gray-500">
            © 2025 AgentForge Web. Powered by AI agents.
          </p>
        </div>
      </footer>
    </div>
  );
};
