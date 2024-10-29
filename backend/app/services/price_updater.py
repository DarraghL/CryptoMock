import logging
from datetime import datetime, timedelta
from app import db
from app.models.price_history import PriceHistory

logger = logging.getLogger(__name__)

class PriceUpdater:
    def __init__(self, price_service):
        self.price_service = price_service
        self.supported_symbols = self.price_service.supported_coins.keys()
        self.last_update = {}
        self.history_retention_days = 30  # Keep 30 days of price history

    def update_prices(self):
        """Update prices for all supported cryptocurrencies"""
        try:
            logger.info("Starting price update...")
            prices = self.price_service.get_all_prices()
            
            for symbol, data in prices.items():
                try:
                    # Store in price history
                    price_history = PriceHistory(
                        crypto_symbol=symbol,
                        price=data['price'],
                        timestamp=datetime.utcnow()
                    )
                    db.session.add(price_history)
                    
                    # Update last update time
                    self.last_update[symbol] = datetime.utcnow()
                    
                except Exception as e:
                    logger.error(f"Error updating price for {symbol}: {str(e)}")
                    continue
            
            db.session.commit()
            logger.info("Price update completed successfully")
            
        except Exception as e:
            logger.error(f"Error during price update: {str(e)}")
            db.session.rollback()

    def cleanup_old_prices(self):
        """Clean up price history older than retention period"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=self.history_retention_days)
            
            PriceHistory.query.filter(
                PriceHistory.timestamp < cutoff_date
            ).delete()
            
            db.session.commit()
            logger.info(f"Cleaned up price history older than {self.history_retention_days} days")
            
        except Exception as e:
            logger.error(f"Error cleaning up price history: {str(e)}")
            db.session.rollback()

    def get_last_update_time(self, symbol):
        """Get last update time for a symbol"""
        return self.last_update.get(symbol)