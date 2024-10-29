import pytest
import os
import logging
from pathlib import Path
from datetime import datetime, timezone
from app import create_app
from app.services import price_updater, price_service
from app.services.scheduler import SchedulerService

# Configure test logging
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)
test_log_file = log_dir / 'test_scheduler.log'

logging.basicConfig(
    filename=str(test_log_file),
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def app():
    """Create test app instance"""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SCHEDULER_API_ENABLED': True,
        'SCHEDULER_TIMEZONE': timezone.utc
    })
    return app

@pytest.fixture(scope='function')
def test_scheduler(app):
    """Create a test scheduler instance"""
    scheduler = SchedulerService()
    yield scheduler
    try:
        if scheduler.is_running:  # Changed from running to is_running
            scheduler.shutdown()
    except Exception as e:
        logger.warning(f"Error shutting down scheduler: {e}")

@pytest.fixture(autouse=True)
def cleanup_logs():
    """Clean up log files after tests"""
    yield
    try:
        for file in Path('logs').glob('*.log*'):
            try:
                file.unlink(missing_ok=True)
            except PermissionError:
                pass
    except Exception as e:
        logger.warning(f"Failed to cleanup logs: {e}")

def test_price_updates(app, test_scheduler):
    """Test that price updates are working"""
    with app.app_context():
        try:
            # Initialize price service
            logger.info("Starting price update test")
            
            # Trigger price update
            print("\nTesting price updates...")
            price_updater.update_prices()  # Changed from update_all_prices to update_prices
            
            # Get latest prices through price service
            prices = price_service.get_all_prices()
            assert isinstance(prices, dict), "Prices should be returned as dictionary"
            assert len(prices) > 0, "Should have at least one price"
            assert 'BTC' in prices, "Bitcoin price should be included"
            
            print("\nLatest prices:")
            for symbol, data in prices.items():
                if isinstance(data, dict) and 'price' in data:
                    print(f"{symbol}: ${data['price']:,.2f}")
                else:
                    print(f"{symbol}: {data}")
            
            logger.info("Price update test completed successfully")

        except Exception as e:
            logger.error(f"Error during test: {str(e)}")
            raise

def test_scheduler_lifecycle(app, test_scheduler):
    """Test scheduler startup and shutdown"""
    with app.app_context():
        try:
            # Test scheduler initialization
            assert not test_scheduler.is_running  # Changed from running to is_running
            test_scheduler.init_app(app, price_updater)
            assert test_scheduler.is_running  # Changed from running to is_running
            
            # Test scheduler shutdown
            test_scheduler.shutdown()
            assert not test_scheduler.is_running  # Changed from running to is_running
            
        except Exception as e:
            logger.error(f"Error testing scheduler lifecycle: {str(e)}")
            raise

if __name__ == "__main__":
    pytest.main([__file__, '-v', '-s'])