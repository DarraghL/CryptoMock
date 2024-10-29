// src/api/market.ts
import axios from './axios';
import { MarketPrice, PriceHistory } from '../types/api';

export const getMarketPrices = async (): Promise<Record<string, MarketPrice>> => {
  // Add timestamp to prevent caching
  const response = await axios.get(`/market/prices?_t=${Date.now()}`);
  return response.data;
};

export const getCryptoPrice = async (symbol: string): Promise<MarketPrice> => {
  const response = await axios.get(`/market/price/${symbol}?_t=${Date.now()}`);
  return response.data;
};

export const getPriceHistory = async (symbol: string): Promise<PriceHistory> => {
  const response = await axios.get(`/market/history/${symbol}`);
  return response.data;
};