// src/pages/Trade.tsx
import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import TradeForm from '../components/trading/TradeForm';
import { useTrading } from '../hooks/useTrading';

const Trade = () => {
  const location = useLocation();
  const { recentTrades, fetchRecentTrades } = useTrading();
  const [selectedTab, setSelectedTab] = useState<'buy' | 'sell'>('buy');

  // Handle initial tab from navigation state
  useEffect(() => {
    const state = location.state as { initialTab?: 'buy' | 'sell' };
    if (state?.initialTab) {
      setSelectedTab(state.initialTab);
    }
  }, [location]);

  useEffect(() => {
    fetchRecentTrades();
  }, []);

  const handleTradeComplete = async () => {
    await fetchRecentTrades();
  };

  const tabs = [
    { id: 'buy', label: 'Buy' },
    { id: 'sell', label: 'Sell' },
  ] as const;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center bg-gray-900/50 backdrop-blur-sm rounded-lg shadow p-6">
        <h1 className="text-2xl font-bold tracking-tight text-gray-100">
          Trade Cryptocurrency
        </h1>
      </div>

      {/* Main Content */}
      <div className="grid gap-6 grid-cols-1 lg:grid-cols-2">
        {/* Trade Form Section */}
        <div className="space-y-4">
          <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg shadow">
            <div className="border-b border-gray-700">
              <nav className="-mb-px flex" aria-label="Tabs">
                {tabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setSelectedTab(tab.id)}
                    className={`
                      w-1/2 py-4 px-1 text-center border-b-2 font-medium text-sm
                      ${selectedTab === tab.id
                        ? 'border-blue-500 text-blue-500'
                        : 'border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-300'
                      }
                    `}
                  >
                    {tab.label}
                  </button>
                ))}
              </nav>
            </div>
            <div className="p-4">
              <TradeForm 
                onTradeComplete={handleTradeComplete} 
                tradeType={selectedTab}
              />
            </div>
          </div>
        </div>

        {/* Recent Trades Section */}
        <div className="space-y-4">
          <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-100 mb-4">Recent Trades</h2>
            <div className="overflow-hidden rounded-lg border border-gray-700">
              <table className="min-w-full divide-y divide-gray-700">
                <thead className="bg-gray-800/50">
                  <tr>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                      Type
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                      Asset
                    </th>
                    <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">
                      Amount
                    </th>
                    <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">
                      Date
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-700">
                  {recentTrades.length > 0 ? (
                    recentTrades.map((trade) => (
                      <tr key={trade.id} className="hover:bg-gray-800/50 transition-colors">
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-100">
                          {trade.transaction_type.toUpperCase()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-100">
                          {trade.crypto_symbol}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-100">
                          ${trade.total_amount.toLocaleString()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-400">
                          {new Date(trade.created_at).toLocaleDateString()}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={4} className="px-6 py-4 whitespace-nowrap text-sm text-center text-gray-400">
                        No recent trades
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Trade;