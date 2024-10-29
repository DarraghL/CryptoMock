// src/hooks/usePortfolio.ts
import { useState, useEffect, useCallback } from 'react';
import { Portfolio } from '../types/models';
import { PortfolioBalance } from '../types/models';
import axios from '../api/axios';

interface UsePortfolioReturn {
  balance: PortfolioBalance | null;
  holdings: Portfolio[];
  loading: boolean;
  error: Error | null;
  refresh: () => Promise<void>;
}

export const usePortfolio = (pollingInterval = 30000): UsePortfolioReturn => {
  const [balance, setBalance] = useState<PortfolioBalance | null>(null);
  const [holdings, setHoldings] = useState<Portfolio[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchPortfolioData = useCallback(async () => {
    try {
      const [balanceResponse, holdingsResponse] = await Promise.all([
        axios.get('/portfolio/balance'),
        axios.get('/portfolio/holdings')
      ]);
      
      setBalance(balanceResponse.data);
      setHoldings(holdingsResponse.data.holdings || []);
      setError(null);
    } catch (err) {
      console.error('Portfolio fetch error:', err);
      setError(err instanceof Error ? err : new Error('Failed to fetch portfolio data'));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchPortfolioData();

    // Set up polling interval
    const intervalId = setInterval(fetchPortfolioData, pollingInterval);

    // Cleanup function to clear interval
    return () => clearInterval(intervalId);
  }, [fetchPortfolioData, pollingInterval]);

  const refresh = useCallback(async () => {
    await fetchPortfolioData();
  }, [fetchPortfolioData]);

  return {
    balance,
    holdings,
    loading,
    error,
    refresh
  };
};