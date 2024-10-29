// src/pages/Portfolio.tsx
import HoldingsTable from '../components/portfolio/HoldingsTable';
import PortfolioSummary from '../components/portfolio/PortfolioSummary';

const Portfolio = () => {
  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg shadow p-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-100">Portfolio</h1>
      </div>

      <PortfolioSummary />
      
      {/* Holdings Section */}
      <div className="bg-gray-900/50 backdrop-blur-sm rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-100">Your Holdings</h2>
        </div>
        <HoldingsTable />
      </div>
    </div>
  );
};

export default Portfolio;