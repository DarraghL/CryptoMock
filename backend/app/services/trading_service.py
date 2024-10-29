from app import db
from app.models.user import User
from app.models.portfolio import Portfolio
from app.models.transaction import Transaction, TransactionType
import logging
from decimal import Decimal
from decimal import Decimal, ROUND_HALF_UP

logger = logging.getLogger(__name__)

class TradingService:
    def __init__(self, price_service):
        self.fee_rate = 0.001  # 0.1% trading fee
        self.price_service = price_service
    
    def init_app(self, app):
        """Initialize with Flask app"""
        self.app = app
    

    def execute_buy(self, user_id, symbol, quantity):
        """
        Execute a buy order for cryptocurrency
        
        Args:
            user_id (int): The user's ID
            symbol (str): The cryptocurrency symbol
            quantity (float): The amount to buy
            
        Returns:
            dict: Result of the transaction
        """
        try:
            # Get current price
            current_price, _ = self.price_service.get_price(symbol)
            if not current_price:
                return {'success': False, 'error': f'Could not get price for {symbol}'}

            # Calculate total cost including fees
            total_cost = float(Decimal(str(quantity)) * Decimal(str(current_price)))
            fee = total_cost * self.fee_rate
            total_with_fees = total_cost + fee

            # Get user
            user = User.query.get(user_id)
            if not user:
                return {'success': False, 'error': 'User not found'}

            # Check if user has enough balance
            if user.current_balance < total_with_fees:
                return {'success': False, 'error': 'Insufficient funds'}

            # Get or create portfolio
            portfolio = Portfolio.query.filter_by(
                user_id=user_id,
                crypto_symbol=symbol
            ).first()

            if portfolio:
                # Update existing portfolio
                new_total = (portfolio.quantity * portfolio.average_buy_price) + total_cost
                new_quantity = portfolio.quantity + quantity
                portfolio.average_buy_price = new_total / new_quantity
                portfolio.quantity = new_quantity
            else:
                # Create new portfolio entry
                portfolio = Portfolio(
                    user_id=user_id,
                    crypto_symbol=symbol,
                    quantity=quantity,
                    average_buy_price=current_price
                )
                db.session.add(portfolio)

            # Create transaction record
            transaction = Transaction(
                user_id=user_id,
                crypto_symbol=symbol,
                transaction_type=TransactionType.BUY,
                quantity=quantity,
                price_per_unit=current_price,
                total_amount=total_cost,
                fee=fee
            )
            db.session.add(transaction)

            # Update user balance
            user.current_balance -= total_with_fees

            # Commit changes
            db.session.commit()

            return {
                'success': True,
                'transaction_id': transaction.id,
                'quantity': quantity,
                'price': current_price,
                'total_cost': total_with_fees,
                'fee': fee
            }

        except Exception as e:
            logger.error(f"Error executing buy order: {str(e)}")
            db.session.rollback()
            return {'success': False, 'error': str(e)}

    def execute_sell(self, user_id, symbol, quantity):
        """
        Execute a sell order for cryptocurrency
        """
        try:
            # Convert quantities to Decimal for precise comparison
            quantity = Decimal(str(quantity)).quantize(Decimal('0.00000001'), rounding=ROUND_HALF_UP)
            
            # Get portfolio
            portfolio = Portfolio.query.filter_by(
                user_id=user_id,
                crypto_symbol=symbol
            ).first()

            if not portfolio:
                return {'success': False, 'error': 'No holdings found for this cryptocurrency'}

            # Convert portfolio quantity to Decimal
            portfolio_quantity = Decimal(str(portfolio.quantity)).quantize(Decimal('0.00000001'), rounding=ROUND_HALF_UP)

            # Check if user has enough crypto
            if portfolio_quantity < quantity:
                return {'success': False, 'error': 'Insufficient crypto balance'}

            # Get current price
            current_price, _ = self.price_service.get_price(symbol)
            if not current_price:
                return {'success': False, 'error': f'Could not get price for {symbol}'}

            # Calculate values using Decimal
            total_value = float(quantity * Decimal(str(current_price)))
            fee = total_value * self.fee_rate
            total_after_fees = total_value - fee

            # Get user
            user = User.query.get(user_id)
            if not user:
                return {'success': False, 'error': 'User not found'}

            # Update portfolio
            new_quantity = portfolio_quantity - quantity
            
            # If quantity is effectively zero (less than smallest unit), remove portfolio entry
            if new_quantity < Decimal('0.00000001'):
                db.session.delete(portfolio)
            else:
                portfolio.quantity = float(new_quantity)

            # Create transaction record
            transaction = Transaction(
                user_id=user_id,
                crypto_symbol=symbol,
                transaction_type=TransactionType.SELL,
                quantity=float(quantity),
                price_per_unit=current_price,
                total_amount=total_value,
                fee=fee
            )
            db.session.add(transaction)

            # Update user balance
            user.current_balance += total_after_fees

            # Commit changes
            db.session.commit()

            return {
                'success': True,
                'transaction_id': transaction.id,
                'quantity': float(quantity),
                'price': current_price,
                'total_value': total_after_fees,
                'fee': fee
            }

        except Exception as e:
            logger.error(f"Error executing sell order: {str(e)}")
            db.session.rollback()
            return {'success': False, 'error': str(e)}

    def get_portfolio_summary(self, user_id):
        """
        Get a summary of user's portfolio
        
        Args:
            user_id (int): The user's ID
            
        Returns:
            dict: Portfolio summary
        """
        try:
            portfolios = Portfolio.query.filter_by(user_id=user_id).all()
            
            holdings = []
            total_value = 0.0
            
            for p in portfolios:
                try:
                    current_price, price_change = self.price_service.get_price(p.crypto_symbol)
                    if current_price:
                        value = p.quantity * current_price
                        holdings.append({
                            'symbol': p.crypto_symbol,
                            'quantity': p.quantity,
                            'average_buy_price': p.average_buy_price,
                            'current_price': current_price,
                            'current_value': value,
                            'profit_loss': value - (p.quantity * p.average_buy_price),
                            'price_change_24h': price_change
                        })
                        total_value += value
                except Exception as e:
                    logger.error(f"Error getting price for {p.crypto_symbol}: {str(e)}")
                    continue

            return {
                'user_id': user_id,
                'holdings': holdings,
                'total_value': total_value
            }
        
    

        except Exception as e:
            logger.error(f"Error getting portfolio summary: {str(e)}")
            return None
    # app/services/trading_service.py
# Add this new method to the TradingService class:

def get_recent_trades(self, user_id, limit=5):
    """
    Get recent trades for a user
    
    Args:
        user_id (int): The user's ID
        limit (int): Number of trades to return
        
    Returns:
        list: Recent transactions
    """
    try:
        recent_transactions = Transaction.query.filter_by(user_id=user_id)\
            .order_by(Transaction.created_at.desc())\
            .limit(limit)\
            .all()
        
        return [tx.to_dict() for tx in recent_transactions]
    except Exception as e:
        logger.error(f"Error getting recent trades: {str(e)}")
        return []