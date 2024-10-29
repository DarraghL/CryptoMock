// src/types/models.ts
export interface User {
    id: number;
    email: string;
    username: string;
    picture?: string;
    current_balance: number;
    created_at: string;
    updated_at: string;
    last_login: string;
}

export interface Portfolio {
    id: number;
    user_id: number;
    crypto_symbol: string;
    quantity: number;
    average_buy_price: number;
    current_value?: number;  // Made optional since it's calculated
    created_at: string;
    updated_at: string;
}

export interface Transaction {
    id: number;
    user_id: number;
    crypto_symbol: string;
    transaction_type: 'buy' | 'sell';
    quantity: number;
    price_per_unit: number;
    total_amount: number;
    fee: number;
    created_at: string;
}

export interface PortfolioBalance {
    cash_balance: number;
    crypto_balance: number;
    total_balance: number;
}