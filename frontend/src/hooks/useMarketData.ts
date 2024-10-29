// src/hooks/useMarketData.ts
import { useState, useEffect, useCallback } from 'react';
import { MarketPrice } from '../types/api';
import { getMarketPrices } from '../api/market';

export const useMarketData = (refreshInterval = 10000) => { // Check every 10 seconds
  const [prices, setPrices] = useState<Record<string, MarketPrice>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date());

  const fetchPrices = useCallback(async () => {
    try {
      const response = await getMarketPrices();
      
      // Check if any prices have changed
      let hasChanges = false;
      Object.entries(response).forEach(([symbol, newData]) => {
        const oldPrice = prices[symbol]?.price;
        if (oldPrice !== newData.price) {
          hasChanges = true;
          console.log(`${symbol} price updated:`, {
            old: oldPrice,
            new: newData.price,
            difference: newData.price - (oldPrice ?? 0),
            timestamp: new Date().toLocaleTimeString()
          });
        }
      });

      // Only update state if there are price changes
      if (hasChanges) {
        console.log('Price changes detected - updating state');
        setPrices(response);
        setLastUpdated(new Date());
      }
      
      setError(null);
    } catch (err) {
      console.error('Price fetch error:', err);
      setError(err instanceof Error ? err : new Error('Failed to fetch prices'));
    } finally {
      setLoading(false);
    }
  }, [prices]);

  // Initial fetch and periodic updates
  useEffect(() => {
    fetchPrices();
    const interval = setInterval(fetchPrices, refreshInterval);
    return () => clearInterval(interval);
  }, [fetchPrices, refreshInterval]);

  return { 
    prices, 
    loading, 
    error, 
    lastUpdated 
  };
};