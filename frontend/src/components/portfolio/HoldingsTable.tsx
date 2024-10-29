// src/components/portfolio/HoldingsTable.tsx
import { usePortfolio } from '../../hooks/usePortfolio';
import { useMarketData } from '../../hooks/useMarketData';
import dogecoinGif from '../../assets/dogecoin.gif';

const HoldingsTable = () => {
  const { holdings, loading } = usePortfolio();
  const { prices, loading: pricesLoading, lastUpdated } = useMarketData();

  if (loading || pricesLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="text-center">
          <img 
            src={dogecoinGif} 
            alt="Loading..."
            className="w-24 h-24 mx-auto mb-4"
          />
          <div className="text-gray-400">
            Loading portfolio data...
          </div>
        </div>
      </div>
    );
  }

  if (!holdings || holdings.length === 0) {
    return (
      <div className="text-center py-8 text-gray-400">
        No holdings found. Start trading to build your portfolio!
      </div>
    );
  }

  return (
    <div>
      <div className="mb-4 text-sm text-gray-400 text-right">
        {lastUpdated && (
          <div className="flex items-center justify-end gap-2">
            <span>Prices last changed: {lastUpdated.toLocaleTimeString()}</span>
          </div>
        )}
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-700">
          <thead className="bg-gray-800/50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                Asset
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">
                Holdings
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">
                Avg. Buy Price
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">
                Current Price
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">
                Value
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">
                Profit/Loss
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700">
            {holdings.map((holding) => {
              const currentPrice = prices[holding.crypto_symbol]?.price ?? holding.average_buy_price;
              const currentValue = holding.quantity * currentPrice;
              const originalValue = holding.quantity * holding.average_buy_price;
              const profitLoss = currentValue - originalValue;
              const profitLossPercentage = originalValue > 0 
                ? ((profitLoss / originalValue) * 100)
                : 0;

              // Don't render row if quantity is 0
              if (holding.quantity === 0) return null;

              return (
                <tr key={holding.crypto_symbol} className="hover:bg-gray-800/50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-100">
                    {holding.crypto_symbol}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-100">
                    {holding.quantity.toLocaleString(undefined, { maximumFractionDigits: 8 })}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-100">
                    ${holding.average_buy_price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-100 font-medium">
                    ${currentPrice.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    <span className="ml-1 text-xs">
                      {prices[holding.crypto_symbol]?.change_24h && (
                        <span className={prices[holding.crypto_symbol].change_24h >= 0 ? 'text-green-400' : 'text-red-400'}>
                          ({prices[holding.crypto_symbol].change_24h.toFixed(2)}%)
                        </span>
                      )}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-100">
                    ${currentValue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm text-right ${
                    profitLoss >= 0 ? 'text-green-400' : 'text-red-400'
                  }`}>
                    ${profitLoss.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} 
                    ({profitLossPercentage.toFixed(2)}%)
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default HoldingsTable;