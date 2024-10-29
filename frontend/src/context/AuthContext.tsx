// src/context/AuthContext.tsx
import { createContext, useContext, useCallback, useState, useMemo, ReactNode, useEffect } from 'react';
import { User } from '../types/models';
import { loginWithGoogle } from '../api/auth';
import axios from '../api/axios';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (googleToken: string) => Promise<void>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Verify token and get user data
  const verifyToken = useCallback(async (token: string) => {
    try {
        console.log('Verifying token...');
        const response = await axios.get('/auth/verify', {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            withCredentials: true
        });
        
        if (response.data.user) {
            console.log('Token verified, user data received');
            setUser(response.data.user);
            return true;
        }
        
        return false;
    } catch (err) {
        console.error('Token verification failed:', err);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        return false;
    }
  }, []);

  // Check authentication status on mount and token change
  useEffect(() => {
    const initAuth = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          console.log('No token found');
          setLoading(false);
          return;
        }

        const isValid = await verifyToken(token);
        if (!isValid) {
          console.log('Token invalid');
          // Try refresh token
          const refreshToken = localStorage.getItem('refresh_token');
          if (refreshToken) {
            try {
              const response = await axios.post('/auth/refresh', {}, {
                headers: { Authorization: `Bearer ${refreshToken}` }
              });
              
              localStorage.setItem('access_token', response.data.access_token);
              await verifyToken(response.data.access_token);
            } catch (refreshError) {
              console.error('Refresh token failed:', refreshError);
            }
          }
        }
      } catch (err) {
        console.error('Auth initialization error:', err);
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, [verifyToken]);

  const login = useCallback(async (googleToken: string) => {
    try {
      console.log('Starting login process...');
      setLoading(true);
      setError(null);

      const response = await loginWithGoogle(googleToken);
      console.log('Login successful, storing tokens');

      // Store tokens
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('refresh_token', response.refresh_token);
      
      // Update user state
      setUser(response.user);
      
      console.log('Login complete');
    } catch (err) {
      console.error('Login error:', err);
      setError(err instanceof Error ? err.message : 'Failed to login');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      console.log('Logging out...');
      
      setUser(null);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      
      // Redirect to login page after logout
      window.location.href = '/login';
      
      console.log('Logout complete');
    } catch (err) {
      console.error('Logout error:', err);
    }
  }, []);

  // Memoized context value
  const value = useMemo(
    () => ({
      user,
      loading,
      error,
      login,
      logout,
    }),
    [user, loading, error, login, logout]
  );

  // Optional loading screen
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthProvider;