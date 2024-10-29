// src/hooks/useTrading.ts
import { useState, useEffect } from 'react';
import { usePortfolio } from './usePortfolio';
import axios from '../api/axios';

interface TradeState {
  loading: boolean;
  error: string | null;
  success: boolean;
  message: string | null;
}

interface Trade {
  id: number;
  transaction_type: string;
  crypto_symbol: string;
  total_amount: number;
  created_at: string;
}

export const useTrading = () => {
  const [tradeState, setTradeState] = useState<TradeState>({
    loading: false,
    error: null,
    success: false,
    message: null,
  });
  
  const [recentTrades, setRecentTrades] = useState<Trade[]>([]);
  const { balance } = usePortfolio();

  const fetchRecentTrades = async () => {
    try {
      const response = await axios.get('/trading/recent');
      setRecentTrades(response.data);
    } catch (error) {
      console.error('Failed to fetch recent trades:', error);
    }
  };

  // Fetch trades on component mount
  useEffect(() => {
    fetchRecentTrades();
  }, []);

  const executeTrade = async (type: 'buy' | 'sell', symbol: string, amount: number) => {
    try {
      setTradeState({
        loading: true,
        error: null,
        success: false,
        message: null,
      });

      const response = await axios.post(`/trading/${type}`, {
        symbol,
        amount
      });

      setTradeState({
        loading: false,
        error: null,
        success: true,
        message: `Successfully ${type === 'buy' ? 'bought' : 'sold'} ${amount} ${symbol}`,
      });

      // Fetch updated trades after successful trade
      await fetchRecentTrades();

      return response.data;
    } catch (err: any) {
      setTradeState({
        loading: false,
        error: err.response?.data?.message || 'Trade execution failed',
        success: false,
        message: null,
      });
      throw err;
    }
  };

  return {
    executeTrade,
    tradeState,
    currentBalance: balance?.cash_balance ?? 0,
    recentTrades,
    fetchRecentTrades
  };
};