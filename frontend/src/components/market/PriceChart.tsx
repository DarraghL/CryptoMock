// src/components/market/PriceChart.tsx
import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { getPriceHistory } from '../../api/market';
import { useMarketData } from '../../hooks/useMarketData';

interface PriceChartProps {
  symbol: string;
}

interface PriceData {
  timestamp: string;
  price: number;
}

const PriceChart: React.FC<PriceChartProps> = ({ symbol }) => {
  const [priceHistory, setPriceHistory] = useState<PriceData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { prices } = useMarketData();

  useEffect(() => {
    const fetchPriceHistory = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await getPriceHistory(symbol);
        
        // Validate response data
        if (!response || !response.history || !Array.isArray(response.history)) {
          throw new Error('Invalid response format');
        }

        // Validate each data point
        const validData = response.history.filter(point => 
          point && 
          typeof point.timestamp === 'string' && 
          typeof point.price === 'number' &&
          !isNaN(point.price)
        );

        if (validData.length === 0) {
          throw new Error('No valid price data available');
        }

        setPriceHistory(validData);
      } catch (err) {
        console.error('Price history fetch error:', err);
        setError(err instanceof Error ? err.message : 'Failed to load price history');
      } finally {
        setLoading(false);
      }
    };

    if (symbol) {
      fetchPriceHistory();
    }
  }, [symbol]);

  // Loading state
  if (loading) {
    return (
      <div className="h-96 bg-gray-900/50 backdrop-blur-sm rounded-lg flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading price history...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="h-96 bg-gray-900/50 backdrop-blur-sm rounded-lg flex items-center justify-center">
        <div className="text-center px-4">
          <p className="text-red-400 mb-2">⚠️ {error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="text-sm text-blue-400 hover:text-fr-300 transition-colors"
          >
            Try again
          </button>
        </div>
      </div>
    );
  }

  // Empty state
  if (!priceHistory.length) {
    return (
      <div className="h-96 bg-gray-900/50 backdrop-blur-sm rounded-lg flex items-center justify-center">
        <p className="text-gray-400">No price data available for {symbol}</p>
      </div>
    );
  }

  const formatDate = (timestamp: string) => {
    try {
      return new Date(timestamp).toLocaleDateString(undefined, {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      });
    } catch (e) {
      return 'Invalid Date';
    }
  };

  const formatPrice = (price: number) => {
    try {
      return `$${price.toLocaleString(undefined, { 
        minimumFractionDigits: 2,
        maximumFractionDigits: 2 
      })}`;
    } catch (e) {
      return '$0.00';
    }
  };

  // Get current price and calculate price change
  const currentPrice = prices[symbol]?.price ?? 0;
  const priceChange = prices[symbol]?.change_24h ?? 0;
  const priceChangeColor = priceChange >= 0 ? 'text-green-400' : 'text-red-400';

  return (
    <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg p-6 space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold text-gray-100">
            {symbol} Price Chart
          </h3>
          <p className="text-sm text-gray-400">
            7 Day Price History
          </p>
        </div>
        <div className="text-right">
          <p className="text-gray-400">Current Price</p>
          <p className="text-xl font-bold text-gray-100">
            {formatPrice(currentPrice)}
          </p>
          <p className={`text-sm ${priceChangeColor}`}>
            {priceChange >= 0 ? '↑' : '↓'} {Math.abs(priceChange).toFixed(2)}%
          </p>
        </div>
      </div>
      
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={priceHistory}
            margin={{ top: 5, right: 5, left: 5, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis 
              dataKey="timestamp" 
              tickFormatter={formatDate} 
              stroke="#9CA3AF"
              tick={{ fill: '#9CA3AF' }}
              minTickGap={50}
            />
            <YAxis 
              tickFormatter={formatPrice} 
              stroke="#9CA3AF"
              tick={{ fill: '#9CA3AF' }}
              domain={['auto', 'auto']}
              width={80}
            />
            <Tooltip 
              formatter={(value: number) => [formatPrice(value), 'Price']}
              labelFormatter={formatDate}
              contentStyle={{ 
                backgroundColor: '#1F2937',
                borderColor: '#374151',
                color: '#E5E7EB',
                borderRadius: '0.375rem',
                padding: '8px'
              }}
            />
            <Line 
              type="monotone" 
              dataKey="price" 
              stroke="#3B82F6" 
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 6, fill: '#3B82F6' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default PriceChart;