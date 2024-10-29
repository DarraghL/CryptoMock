// src/pages/Market.tsx
import { useState } from 'react';
import PriceTable from '../components/market/PriceTable';
import PriceChart from '../components/market/PriceChart';

const Market = () => {
  const [selectedCrypto, setSelectedCrypto] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'prices' | 'charts'>('prices');

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg shadow p-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-100">Market Overview</h1>
      </div>

      {/* Main Content */}
      <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg shadow">
        {/* Tabs Navigation */}
        <div className="border-b border-gray-700">
          <nav className="-mb-px flex" aria-label="Tabs">
            <button
              onClick={() => setActiveTab('prices')}
              className={`w-1/2 py-4 px-1 text-center border-b-2 font-medium text-sm transition-colors duration-200 ${
                activeTab === 'prices'
                  ? 'border-blue-500 text-blue-400'
                  : 'border-transparent text-gray-400 hover:text-green-300 hover:border-green-600'
              }`}
            >
              Live Prices
            </button>
            <button
              onClick={() => setActiveTab('charts')}
              className={`w-1/2 py-4 px-1 text-center border-b-2 font-medium text-sm transition-colors duration-200 ${
                activeTab === 'charts'
                  ? 'border-blue-500 text-blue-400'
                  : 'border-transparent text-gray-400 hover:text-green-300 hover:border-green-600'
              }`}
            >
              Price Charts
            </button>
          </nav>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {activeTab === 'prices' ? (
            <div className="space-y-4">
              <PriceTable onSelectCrypto={setSelectedCrypto} />
            </div>
          ) : (
            <div className="space-y-4">
              {selectedCrypto ? (
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <h2 className="text-xl font-semibold text-gray-100">
                      Price Chart
                    </h2>
                    <button
                      onClick={() => setSelectedCrypto(null)}
                      className="text-sm text-blue-400 hover:text-green-300 transition-colors"
                    >
                      Change Cryptocurrency
                    </button>
                  </div>
                  <PriceChart symbol={selectedCrypto} />
                </div>
              ) : (
                <div className="text-center py-12 bg-gray-800/50 rounded-lg">
                  <div className="text-gray-400">
                    Select a cryptocurrency from the price table to view its chart
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Table/Chart Navigation - Only show when in chart mode */}
      {activeTab === 'charts' && !selectedCrypto && (
        <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-100 mb-4">
            Available Cryptocurrencies
          </h3>
          <div className="space-y-4">
            <PriceTable 
              onSelectCrypto={setSelectedCrypto}
              //  // Add compact prop to PriceTable
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default Market;