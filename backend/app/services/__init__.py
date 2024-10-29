import logging
from .price_service import PriceService
from .trading_service import TradingService
from .price_updater import PriceUpdater
from .scheduler import SchedulerService

# Set up logger
logger = logging.getLogger(__name__)

# Create service instances
price_service = PriceService()
trading_service = TradingService(price_service)
price_updater = PriceUpdater(price_service)
scheduler = SchedulerService()

def init_app(app):
    """Initialize all services with app context"""
    try:
        # Initialize price service first
        price_service.init_app(app)
        
        # Then initialize trading service
        trading_service.init_app(app)
        
        # Initialize scheduler last
        scheduler.init_app(app, price_updater)
        
        logger.info("All services initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing services: {str(e)}")
        raise

__all__ = [
    'price_service',
    'trading_service',
    'price_updater',
    'scheduler',
    'init_app'
]