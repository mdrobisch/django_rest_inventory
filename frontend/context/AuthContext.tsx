import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import api from '../api';
import { saveToken, getToken, removeToken } from '../utils/storage';

interface AuthContextType {
  token: string | null;
  signIn: (username: string, password: string) => Promise<boolean>;
  signOut: () => Promise<void>;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadToken = async () => {
      const storedToken = await getToken();
      setToken(storedToken);
      setIsLoading(false);
    };
    loadToken();
  }, []);

  const signIn = async (username: string, password: string) => {
    try {
      const response = await api.post('/auth/token/', { username, password });
      const access = response.data.access;
      await saveToken(access);
      setToken(access);
      return true;
    } catch (error) {
      return false;
    }
  };

  const signOut = async () => {
    await removeToken();
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ token, signIn, signOut, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
