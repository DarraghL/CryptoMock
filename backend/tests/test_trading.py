import pytest
from decimal import Decimal
from app.services import trading_service, price_service
from app.models.portfolio import Portfolio

# Test constants
TEST_SYMBOL = 'BTC'
TEST_BUY_AMOUNT = Decimal('0.1')

def verify_portfolio(user_id, symbol, expected_quantity):
    """Helper function to verify portfolio quantity"""
    portfolio = Portfolio.query.filter_by(
        user_id=user_id,
        crypto_symbol=symbol
    ).first()
    
    assert portfolio is not None, f"Portfolio for {symbol} should exist"
    assert abs(Decimal(str(portfolio.quantity)) - expected_quantity) < Decimal('0.00001'), \
        f"Expected {expected_quantity} {symbol}, but got {portfolio.quantity}"
    
    return portfolio

def test_trading_flow(app, db_session, test_user, caplog, disable_logging):
    """Test complete trading flow: buy and sell with proper cleanup"""
    with app.app_context():
        try:
            # Initial state verification
            assert test_user.current_balance == Decimal('100000.0'), \
                "Initial balance should match test user setup"
            
            # Get current market price
            current_price, change_24h = price_service.get_price(TEST_SYMBOL)
            print(f"\nTest buying {TEST_BUY_AMOUNT} {TEST_SYMBOL} at ${current_price:,.2f}")
            
            # Execute buy order
            buy_result = trading_service.execute_buy(
                test_user.id,
                TEST_SYMBOL,
                float(TEST_BUY_AMOUNT)  # Convert Decimal to float for the service
            )
            
            # Verify buy result
            assert buy_result['success'], f"Buy order failed: {buy_result.get('error', 'Unknown error')}"
            verify_portfolio(test_user.id, TEST_SYMBOL, TEST_BUY_AMOUNT)
            
            # Test selling half position
            sell_amount = TEST_BUY_AMOUNT / 2
            print(f"\nTest selling {sell_amount} {TEST_SYMBOL}")
            
            # Execute sell order
            sell_result = trading_service.execute_sell(
                test_user.id,
                TEST_SYMBOL,
                float(sell_amount)  # Convert Decimal to float for the service
            )
            
            # Verify sell result
            assert sell_result['success'], f"Sell order failed: {sell_result.get('error', 'Unknown error')}"
            verify_portfolio(test_user.id, TEST_SYMBOL, TEST_BUY_AMOUNT - sell_amount)
            
            # Verify portfolio summary
            summary = trading_service.get_portfolio_summary(test_user.id)
            assert summary is not None, "Portfolio summary should exist"
            assert TEST_SYMBOL in [holding['symbol'] for holding in summary['holdings']], \
                f"{TEST_SYMBOL} should be in portfolio summary"
            
        except Exception as e:
            db_session.rollback()
            pytest.fail(f"Test failed: {str(e)}")

if __name__ == "__main__":
    pytest.main([__file__, '-v'])