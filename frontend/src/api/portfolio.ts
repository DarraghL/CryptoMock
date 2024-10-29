import axios from './axios';
import { PortfolioBalance } from '../types/api';
import { Portfolio } from '../types/models';

export const getPortfolioBalance = async (): Promise<PortfolioBalance> => {
  const response = await axios.get('/portfolio/balance');
  return response.data;
};

export const getHoldings = async (): Promise<Portfolio[]> => {
  const response = await axios.get('/portfolio/holdings');
  return response.data.holdings;
};