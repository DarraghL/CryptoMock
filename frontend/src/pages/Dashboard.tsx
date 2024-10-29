// src/pages/Dashboard.tsx
import { useNavigate } from 'react-router-dom';
import PortfolioSummary from '../components/portfolio/PortfolioSummary';
import HoldingsTable from '../components/portfolio/HoldingsTable';
import PriceTable from '../components/market/PriceTable';
import { useAuth } from '../context/AuthContext';
import { useTrading } from '../hooks/useTrading';
import { useEffect } from 'react';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const { recentTrades, fetchRecentTrades } = useTrading();
  useEffect(() => {
    fetchRecentTrades();
  }, []);

  // Button handlers
  const handleBuyCrypto = () => navigate('/trade', { state: { initialTab: 'buy' } });
  const handleSellCrypto = () => navigate('/trade', { state: { initialTab: 'sell' } });
  const handleViewPortfolio = () => navigate('/portfolio');
  const handleViewAllActivity = () => navigate('/portfolio', { state: { section: 'activity' } });

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="flex justify-between items-center bg-gray-900/50 backdrop-blur-sm rounded-lg shadow p-6">
        <h1 className="text-2xl font-bold tracking-tight text-gray-100">
          Welcome back, {user?.username}
        </h1>
      </div>

      {/* Portfolio Overview */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg shadow p-6 col-span-full">
          <div className="grid gap-4">
            <h2 className="text-xl font-semibold text-gray-100">Total Balance</h2>
            <PortfolioSummary />
          </div>
        </div>
      </div>

      {/* Market Overview */}
      <div className="grid gap-4 grid-cols-1 lg:grid-cols-2">
        {/* Market Overview Card */}
        <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg shadow p-6">
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-100">Market Overview</h2>
            <div className="overflow-hidden">
              <PriceTable limit={5} />
            </div>
          </div>
        </div>

        {/* Holdings Card */}
        <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg shadow p-6">
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-100">Your Holdings</h2>
            <div className="overflow-hidden">
              <HoldingsTable />
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity Section */}
      <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg shadow p-6">
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-semibold text-gray-100">Recent Activity</h2>
            <button 
              onClick={handleViewAllActivity}
              className="text-sm text-blue-400 hover:text-blue-300 transition-colors"
            >
              View All
            </button>
          </div>
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

      {/* Quick Actions */}
      <div className="grid gap-4 grid-cols-1 md:grid-cols-3">
        <button 
          onClick={handleBuyCrypto}
          className="p-4 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
        >
          Buy Crypto
        </button>
        <button 
          onClick={handleSellCrypto}
          className="p-4 bg-green-600 text-white rounded-lg shadow hover:bg-green-700 transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
        >
          Sell Crypto
        </button>
        <button 
          onClick={handleViewPortfolio}
          className="p-4 bg-purple-600 text-white rounded-lg shadow hover:bg-purple-700 transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-opacity-50"
        >
          View Portfolio
        </button>
      </div>
    </div>
  );
};

export default Dashboard;