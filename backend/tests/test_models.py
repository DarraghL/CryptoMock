import pytest
from datetime import datetime, timedelta
from app import create_app, db
from app.models import (
    User, Portfolio, Transaction, TransactionType,
    PriceHistory, WatchlistItem
)

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_session(app):
    """Create database and tables"""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

def test_user_model(db_session):
    """Test User model"""
    # Create test user
    user = User(
        email='test@example.com',
        username='testuser',
        picture='http://example.com/pic.jpg',
        initial_balance=100000.0,
        current_balance=95000.0
    )
    
    db_session.session.add(user)
    db_session.session.commit()

    # Test user creation
    assert user.id is not None
    assert user.email == 'test@example.com'
    assert user.current_balance == 95000.0
    assert user.created_at is not None
    assert user.updated_at is not None

    # Test user to_dict method
    user_dict = user.to_dict()
    assert user_dict['email'] == 'test@example.com'
    assert user_dict['username'] == 'testuser'
    assert user_dict['current_balance'] == 95000.0

    return user  # Return for use in other tests

def test_portfolio_model(db_session):
    """Test Portfolio model"""
    # Create test user first
    user = test_user_model(db_session)
    
    # Create portfolio entry
    portfolio = Portfolio(
        user_id=user.id,
        crypto_symbol='BTC',
        quantity=0.5,
        average_buy_price=50000.0
    )
    
    db_session.session.add(portfolio)
    db_session.session.commit()

    # Test portfolio creation
    assert portfolio.id is not None
    assert portfolio.user_id == user.id
    assert portfolio.crypto_symbol == 'BTC'
    assert portfolio.quantity == 0.5

    # Test portfolio to_dict method
    portfolio_dict = portfolio.to_dict()
    assert portfolio_dict['crypto_symbol'] == 'BTC'
    assert portfolio_dict['quantity'] == 0.5
    assert portfolio_dict['current_value'] == 0.5 * 50000.0

    # Test unique constraint
    with pytest.raises(Exception):
        duplicate_portfolio = Portfolio(
            user_id=user.id,
            crypto_symbol='BTC',
            quantity=1.0,
            average_buy_price=48000.0
        )
        db_session.session.add(duplicate_portfolio)
        db_session.session.commit()

def test_transaction_model(db_session):
    """Test Transaction model"""
    user = test_user_model(db_session)
    
    # Create buy transaction
    transaction = Transaction(
        user_id=user.id,
        crypto_symbol='ETH',
        transaction_type=TransactionType.BUY,
        quantity=2.0,
        price_per_unit=3000.0,
        total_amount=6000.0,
        fee=6.0
    )
    
    db_session.session.add(transaction)
    db_session.session.commit()

    # Test transaction creation
    assert transaction.id is not None
    assert transaction.user_id == user.id
    assert transaction.transaction_type == TransactionType.BUY
    assert transaction.total_amount == 6000.0

    # Test transaction to_dict method
    transaction_dict = transaction.to_dict()
    assert transaction_dict['crypto_symbol'] == 'ETH'
    assert transaction_dict['transaction_type'] == 'buy'
    assert transaction_dict['quantity'] == 2.0

def test_price_history_model(db_session):
    """Test PriceHistory model"""
    # Create price history entry
    price_history = PriceHistory(
        crypto_symbol='BTC',
        price_usd=55000.0,
        volume_24h=1000000.0,
        market_cap=1000000000.0,
        timestamp=datetime.utcnow()
    )
    
    db_session.session.add(price_history)
    db_session.session.commit()

    # Test price history creation
    assert price_history.id is not None
    assert price_history.crypto_symbol == 'BTC'
    assert price_history.price_usd == 55000.0

    # Test price history to_dict method
    price_dict = price_history.to_dict()
    assert price_dict['crypto_symbol'] == 'BTC'
    assert price_dict['price_usd'] == 55000.0
    assert 'timestamp' in price_dict

def test_watchlist_model(db_session):
    """Test WatchlistItem model"""
    user = test_user_model(db_session)
    
    # Create watchlist item
    watchlist_item = WatchlistItem(
        user_id=user.id,
        crypto_symbol='ADA',
        notes='Interesting project'
    )
    
    db_session.session.add(watchlist_item)
    db_session.session.commit()

    # Test watchlist item creation
    assert watchlist_item.id is not None
    assert watchlist_item.user_id == user.id
    assert watchlist_item.crypto_symbol == 'ADA'

    # Test watchlist to_dict method
    watchlist_dict = watchlist_item.to_dict()
    assert watchlist_dict['crypto_symbol'] == 'ADA'
    assert watchlist_dict['notes'] == 'Interesting project'

    # Test unique constraint
    with pytest.raises(Exception):
        duplicate_watchlist = WatchlistItem(
            user_id=user.id,
            crypto_symbol='ADA',
            notes='Another note'
        )
        db_session.session.add(duplicate_watchlist)
        db_session.session.commit()

def test_relationships(db_session):
    """Test relationships between models"""
    # Create user
    user = test_user_model(db_session)
    
    # Add portfolio
    portfolio = Portfolio(
        user_id=user.id,
        crypto_symbol='BTC',
        quantity=1.0,
        average_buy_price=45000.0
    )
    db_session.session.add(portfolio)
    
    # Add transaction
    transaction = Transaction(
        user_id=user.id,
        crypto_symbol='BTC',
        transaction_type=TransactionType.BUY,
        quantity=1.0,
        price_per_unit=45000.0,
        total_amount=45000.0,
        fee=45.0
    )
    db_session.session.add(transaction)
    
    # Add watchlist item
    watchlist = WatchlistItem(
        user_id=user.id,
        crypto_symbol='ETH',
        notes='Watch ETH'
    )
    db_session.session.add(watchlist)
    
    db_session.session.commit()

    # Test relationships
    assert len(user.portfolios) == 1
    assert len(user.transactions) == 1
    assert len(user.watchlist_items) == 1
    assert user.portfolios[0].crypto_symbol == 'BTC'
    assert user.transactions[0].crypto_symbol == 'BTC'
    assert user.watchlist_items[0].crypto_symbol == 'ETH'

def test_timestamps(db_session):
    """Test TimestampMixin functionality"""
    user = test_user_model(db_session)
    created_at = user.created_at
    
    # Update user
    user.username = 'updated_username'
    db_session.session.commit()
    
    # Check timestamps
    assert user.created_at == created_at  # Should not change
    assert user.updated_at > created_at  # Should be updated

if __name__ == "__main__":
    pytest.main([__file__, '-v', '-s'])