// src/components/trading/OrderBook.tsx
import { useState, useEffect } from 'react';
import axios from '../../api/axios';

interface Transaction {
  id: number;
  transaction_type: 'buy' | 'sell';
  crypto_symbol: string;
  quantity: number;
  price_per_unit: number;
  created_at: string;
}

interface OrderBookProps {
  refreshTrigger?: number;
}

const OrderBook: React.FC<OrderBookProps> = ({ refreshTrigger = 0 }) => {
  const [trades, setTrades] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTrades = async () => {
      try {
        setLoading(true);
        const response = await axios.get('/user/transactions');
        // Sort trades by created_at in descending order (newest first)
        const sortedTrades = response.data.transactions.sort((a: Transaction, b: Transaction) => 
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );
        setTrades(sortedTrades);
      } catch (error) {
        console.error('Failed to fetch trades:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTrades();
  }, [refreshTrigger]);

  // Rest of your component remains the same...
  if (loading) {
    return (
      <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-100 mb-4">Recent Trades</h2>
        <div className="animate-pulse space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-16 bg-gray-800 rounded" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold text-gray-100 mb-4">Recent Trades</h2>
      <div className="space-y-4">
        {trades.length > 0 ? (
          trades.map((trade) => (
            <div
              key={trade.id}
              className="flex justify-between items-center p-4 bg-gray-800/50 rounded-lg"
            >
              <div>
                <div className={`text-sm font-medium ${
                  trade.transaction_type === 'buy' ? 'text-green-400' : 'text-red-400'
                }`}>
                  {trade.transaction_type.toUpperCase()} {trade.crypto_symbol}
                </div>
                <div className="text-sm text-gray-400">
                  Amount: {trade.quantity} {trade.crypto_symbol}
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm font-medium text-gray-200">
                  ${trade.price_per_unit.toLocaleString()}
                </div>
                <div className="text-xs text-gray-400">
                  {new Date(trade.created_at).toLocaleString()}
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center text-gray-400 py-8">
            No recent trades
          </div>
        )}
      </div>
    </div>
  );
};

export default OrderBook;