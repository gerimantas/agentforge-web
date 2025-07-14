/**
 * Authentication hook for managing user state and auth operations
 */

import { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import { User, LoginRequest, RegisterRequest, Token } from '../types/agent';
import apiService from '../services/api';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginRequest) => Promise<{ success: boolean; error?: string }>;
  register: (credentials: RegisterRequest) => Promise<{ success: boolean; error?: string }>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = !!user;

  useEffect(() => {
    // Check if user is already logged in on app start
    const checkAuth = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        apiService.setToken(token);
        const response = await apiService.getCurrentUser();
        if (response.data) {
          setUser(response.data as User);
        } else {
          // Token is invalid, remove it
          localStorage.removeItem('access_token');
          apiService.setToken(null);
        }
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (credentials: LoginRequest) => {
    try {
      const response = await apiService.login(credentials.email, credentials.password);
      
      if (response.data) {
        const tokenData = response.data as Token;
        apiService.setToken(tokenData.access_token);
        
        // Get user data
        const userResponse = await apiService.getCurrentUser();
        if (userResponse.data) {
          setUser(userResponse.data as User);
          return { success: true };
        }
      }
      
      return { success: false, error: response.error || 'Login failed' };
    } catch (error) {
      return { success: false, error: 'Login failed' };
    }
  };

  const register = async (credentials: RegisterRequest) => {
    try {
      const response = await apiService.register(credentials.email, credentials.password);
      
      if (response.data) {
        // After successful registration, automatically log in
        return await login(credentials);
      }
      
      return { success: false, error: response.error || 'Registration failed' };
    } catch (error) {
      return { success: false, error: 'Registration failed' };
    }
  };

  const logout = () => {
    setUser(null);
    apiService.setToken(null);
  };

  const value = {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
