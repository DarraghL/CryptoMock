// src/components/market/PriceTable.tsx
import { useMarketData } from '../../hooks/useMarketData';
//import dogecoinGif from '../../assets/dogecoin.gif';

interface PriceTableProps {
  limit?: number;
  onSelectCrypto?: (symbol: string) => void;
}

const PriceTable = ({ limit, onSelectCrypto }: PriceTableProps) => {
  const { prices, loading, error } = useMarketData();

  if (loading) {
    return (
      <div className="animate-pulse space-y-4">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="h-10 bg-gray-200 rounded" />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500 p-4 bg-red-50 rounded">
        Error loading market data: {error.message}
      </div>
    );
  }

  let displayPrices = Object.entries(prices);
  if (limit) {
    displayPrices = displayPrices.slice(0, limit);
  }

  return (
    <div className="overflow-x-auto bg-white rounded-lg shadow">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Cryptocurrency
            </th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              Price
            </th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              24h Change
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {displayPrices.map(([symbol, data]) => (
            <tr
              key={symbol}
              onClick={() => onSelectCrypto?.(symbol)}
              className={`${
                onSelectCrypto ? 'cursor-pointer hover:bg-gray-50' : ''
              }`}
            >
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm font-medium text-gray-900">
                  {symbol}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                ${data.price.toLocaleString()}
              </td>
              <td
                className={`px-6 py-4 whitespace-nowrap text-right text-sm font-medium ${
                  data.change_24h >= 0 ? 'text-green-600' : 'text-red-600'
                }`}
              >
                {data.change_24h >= 0 ? '+' : ''}
                {data.change_24h.toFixed(2)}%
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PriceTable;