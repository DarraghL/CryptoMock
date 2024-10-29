import { useState } from 'react';
import { useTrading } from '../../hooks/useTrading';
import { useMarketData } from '../../hooks/useMarketData';
import { usePortfolio } from '../../hooks/usePortfolio'; // Add this import

interface TradeFormProps {
  onTradeComplete: () => void;
  tradeType: 'buy' | 'sell';
}

const TradeForm: React.FC<TradeFormProps> = ({ onTradeComplete, tradeType }) => {
  const [symbol, setSymbol] = useState('BTC');
  const [amount, setAmount] = useState('');
  
  const { executeTrade, tradeState, currentBalance } = useTrading();
  const { prices, loading: pricesLoading } = useMarketData();
  const { holdings } = usePortfolio(); // Add this hook

  // Get current holding for selected symbol
  const currentHolding = holdings.find(h => h.crypto_symbol === symbol);
  const availableAmount = currentHolding?.quantity || 0;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!amount || isNaN(Number(amount))) return;
    
    // Add sell validation
    if (tradeType === 'sell' && Number(amount) > availableAmount) {
      console.error('Insufficient balance');
      return;
    }

    try {
      await executeTrade(tradeType, symbol, Number(amount));
      setAmount(''); // Clear form
      if (onTradeComplete) {
        onTradeComplete(); // Call the callback to refresh trades
      }
    } catch (error) {
      console.error('Trade failed:', error);
    }
  };

  const currentPrice = prices[symbol]?.price ?? 0;
  const estimatedCost = currentPrice * Number(amount || 0);
  const canAfford = tradeType === 'sell' 
    ? Number(amount) <= availableAmount 
    : estimatedCost <= currentBalance;

  return (
    <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg shadow p-6">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-100">
            Cryptocurrency
          </label>
          <select
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
            className="mt-1 block w-full pl-3 pr-10 py-2 text-base bg-gray-800 border-gray-700 text-gray-100 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
          >
            {Object.keys(prices).map((sym) => (
              <option key={sym} value={sym}>
                {sym}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-100">
            Amount
          </label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            className="mt-1 block w-full pl-3 pr-10 py-2 text-base bg-gray-800 border-gray-700 text-gray-100 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            placeholder="0.00"
            step="0.0001"
            min="0"
            max={tradeType === 'sell' ? availableAmount : undefined}
          />
        </div>

        {/* Add available balance for sell orders */}
        {tradeType === 'sell' && (
          <div className="text-sm text-gray-300">
            Available {symbol}: {availableAmount.toLocaleString()}
          </div>
        )}

        {amount && (
          <div className="bg-gray-800/50 p-4 rounded-md">
            <p className="text-sm text-gray-300">
              Estimated {tradeType === 'buy' ? 'Cost' : 'Receive'}: ${estimatedCost.toLocaleString()}
            </p>
            {tradeType === 'buy' && (
              <p className="text-sm text-gray-300">
                Available Balance: ${currentBalance.toLocaleString()}
              </p>
            )}
          </div>
        )}

        {tradeState.error && (
          <div className="bg-red-900/50 text-red-300 p-4 rounded-md text-sm">
            {tradeState.error}
          </div>
        )}

        {!canAfford && amount && (
          <div className="bg-red-900/50 text-red-300 p-4 rounded-md text-sm">
            {tradeType === 'sell' 
              ? `Insufficient ${symbol} balance` 
              : 'Insufficient funds'}
          </div>
        )}

        {tradeState.success && tradeState.message && (
          <div className="bg-green-900/50 text-green-300 p-4 rounded-md text-sm">
            {tradeState.message}
          </div>
        )}

        <button
          type="submit"
          disabled={!amount || !canAfford || tradeState.loading || pricesLoading}
          className={`w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white transition-all duration-200 
            ${canAfford && amount
              ? tradeType === 'buy' 
                ? 'bg-blue-600 hover:bg-blue-700'
                : 'bg-green-600 hover:bg-green-700'
              : 'bg-gray-700 cursor-not-allowed'
            } ${tradeState.loading ? 'opacity-50 cursor-wait' : ''}`}
        >
          {tradeState.loading
            ? 'Processing...'
            : `${tradeType === 'buy' ? 'Buy' : 'Sell'} ${symbol}`}
        </button>
      </form>
    </div>
  );
};

export default TradeForm;