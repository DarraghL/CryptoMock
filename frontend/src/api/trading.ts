// src/api/trading.ts
import axios from './axios';
import {TradeResponse } from '../types/api';

export const executeBuyOrder = async (symbol: string, amount: number): Promise<TradeResponse> => {
  const response = await axios.post('/trading/buy', { symbol, amount });
  return response.data;
};

export const executeSellOrder = async (symbol: string, amount: number): Promise<TradeResponse> => {
  const response = await axios.post('/trading/sell', { symbol, amount });
  return response.data;
};

export const getRecentTrades = async (): Promise<any[]> => {
  const response = await axios.get('/trading/recent');
  return response.data;
};