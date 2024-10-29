import axios, { isAxiosError } from 'axios';
import { LoginResponse } from '../types/api';

const API_URL = import.meta.env.VITE_API_URL;

export const loginWithGoogle = async (token: string): Promise<LoginResponse> => {
  try {
    console.log('Sending Google token to backend...');
    const response = await axios.post(`${API_URL}/auth/google`, { token }, {
      headers: {
        'Content-Type': 'application/json'
      },
      withCredentials: true
    });
    console.log('Backend response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Backend error:', error);
    if (isAxiosError(error)) {
      if (error.response) {
        console.error('Response error:', error.response.data);
      }
    }
    throw new Error('Authentication failed');
  }
};