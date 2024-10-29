// src/components/portfolio/PortfolioSummary.tsx
import { usePortfolio } from '../../hooks/usePortfolio';

const PortfolioSummary = () => {
  const { balance, loading, error } = usePortfolio();

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-24 mb-2"></div>
          <div className="h-8 bg-gray-200 rounded w-48"></div>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-20 mb-2"></div>
            <div className="h-6 bg-gray-200 rounded w-32"></div>
          </div>
          <div className="animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-20 mb-2"></div>
            <div className="h-6 bg-gray-200 rounded w-32"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <div className="flex items-center text-red-600">
          <svg className="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
          Error loading portfolio data
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-6">
        <p className="text-sm font-medium text-gray-500">Total Portfolio Value</p>
        <p className="text-4xl font-bold text-green-900 mt-2">
          ${balance?.total_balance.toLocaleString()}
        </p>
        <p className="text-sm text-gray-500 mt-2">
          Updated {new Date().toLocaleTimeString()}
        </p>
      </div>
      <div className="grid grid-cols-2 gap-8">
        <div className="bg-gray-50 rounded-lg p-4">
          <p className="text-sm font-medium text-gray-500">Cash Balance</p>
          <p className="text-2xl font-semibold text-gray-900 mt-2">
            ${balance?.cash_balance.toLocaleString()}
          </p>
        </div>
        <div className="bg-gray-50 rounded-lg p-4">
          <p className="text-sm font-medium text-gray-500">Crypto Balance</p>
          <p className="text-2xl font-semibold text-gray-900 mt-2">
            ${balance?.crypto_balance.toLocaleString()}
          </p>
        </div>
      </div>
    </div>
  );
};

export default PortfolioSummary;