// src/types/api.ts
import { User, Transaction, Portfolio } from './models';
import type { PortfolioBalance } from './models';  // Import as type

// Generic API Response
export interface ApiResponse<T> {
    data?: T;
    error?: string;
    message?: string;
}

// Auth Responses
export interface LoginResponse {
    message: string;
    access_token: string;
    refresh_token: string;
    user: User;
}

// Market Data
export interface MarketPrice {
    symbol: string;
    price: number;
    change_24h: number;
}

export interface PriceHistory {
    symbol: string;
    history: {
        timestamp: string;
        price: number;
    }[];
}

// Portfolio Responses
export interface PortfolioResponse {
    holdings: Portfolio[];
}

export type { PortfolioBalance };  // Re-export as type

// Trading
export interface TradeRequest {
    symbol: string;
    amount: number;
}

export interface TradeResponse {
    success: boolean;
    message?: string;
    transaction_id?: number;
    quantity?: number;
    price?: number;
    total_cost?: number;
    fee?: number;
    transaction?: Transaction;
    new_balance?: number;
}

// Holdings
export interface HoldingsResponse {
    holdings: Portfolio[];
}

// Recent Trades
export interface RecentTradesResponse {
    trades: Transaction[];
}