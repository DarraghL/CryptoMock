// src/api/axios.ts
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

// Debug log the API URL during initialization
console.log('Initializing axios with API URL:', API_URL);

const axiosInstance = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  // Add timeout
  timeout: 10000,
  // Add responseType
  responseType: 'json'
});

// Request interceptor for logging and authorization
axiosInstance.interceptors.request.use(
  (config) => {
    // Log the full request URL
    console.log(`Making ${config.method?.toUpperCase()} request to: ${config.baseURL}${config.url}`);
    
    // Add authorization token if available
    const token = localStorage.getItem('access_token');
    if (token && !config.headers['X-Skip-Interceptor']) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Add CORS headers
    config.headers['Access-Control-Allow-Origin'] = [
      'https://cryptomock.ie',
      'http://localhost:5173'
    ];
    config.headers['Access-Control-Allow-Credentials'] = true;
    
    // Log headers for debugging
    console.log('Request headers:', config.headers);
    
    return config;
  },
  (error) => {
    console.error('Request setup error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for handling responses and errors
axiosInstance.interceptors.response.use(
  (response) => {
    console.log('Response received:', {
      url: response.config.url,
      status: response.status,
      statusText: response.statusText
    });
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    // Handle token refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      console.log('Attempting token refresh...');
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }

        // Attempt to refresh the token
        const response = await axiosInstance.post('/auth/refresh', {}, {
          headers: { 
            Authorization: `Bearer ${refreshToken}`,
            'X-Skip-Interceptor': 'true'
          }
        });

        const { access_token } = response.data;
        console.log('Token refresh successful');
        
        // Update stored token
        localStorage.setItem('access_token', access_token);
        
        // Update the original request's authorization header
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        
        // Retry the original request
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError);
        
        // Clear tokens
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        
        // Handle redirect
        if (!window.location.pathname.includes('/login')) {
          console.log('Redirecting to login page...');
          // Use window.location.replace for a clean redirect
          window.location.replace('/login');
        }
        
        return Promise.reject(refreshError);
      }
    }

    // Handle CORS errors specifically
    if (error.response?.status === 0 || error.code === 'ERR_NETWORK') {
      console.error('CORS or Network Error:', {
        url: originalRequest?.url,
        method: originalRequest?.method,
        error: error.message
      });
      return Promise.reject(new Error('Network error - please check your connection'));
    }

    // Handle other types of errors
    if (error.response) {
      console.error('Server error response:', {
        status: error.response.status,
        data: error.response.data,
        url: originalRequest?.url
      });
      return Promise.reject(error.response.data);
    } else if (error.request) {
      console.error('No response received for request:', {
        url: originalRequest?.url,
        method: originalRequest?.method
      });
      return Promise.reject(new Error('No response received from server'));
    } else {
      console.error('Request setup error:', error.message);
      return Promise.reject(error);
    }
  }
);

// Add response type interceptor
axiosInstance.interceptors.request.use((config) => {
  config.responseType = 'json';
  return config;
});

// Export the configured instance
export default axiosInstance;

// Export a helper function to check configuration
export const checkApiConfiguration = () => {
  console.log({
    API_URL,
    hasAccessToken: !!localStorage.getItem('access_token'),
    hasRefreshToken: !!localStorage.getItem('refresh_token'),
    currentPath: window.location.pathname,
    baseURL: axiosInstance.defaults.baseURL,
    timeout: axiosInstance.defaults.timeout,
    headers: axiosInstance.defaults.headers
  });
};

// Export a function to clear auth state
export const clearAuthState = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  // Clear any default headers
  delete axiosInstance.defaults.headers.common['Authorization'];
};

// Export a function to set auth token
export const setAuthToken = (token: string) => {
  if (token) {
    localStorage.setItem('access_token', token);
    axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }
};