import pytest
from decimal import Decimal
from pathlib import Path
from app import create_app, db
from app.models.user import User
from app.models.portfolio import Portfolio
from app.models.transaction import Transaction

# Test constants
TEST_USER = {
    'email': 'test@example.com',
    'username': 'test_user',
    'initial_balance': Decimal('100000.0')
}

@pytest.fixture(scope='session')
def app():
    """Create test application"""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgresql://daz:darragh1@localhost:5432/stocksim_test',
        'SCHEDULER_API_ENABLED': True
    })
    return app

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def db_session(app):
    """Create database and tables"""
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def test_user(app, db_session):
    """Fixture to create and clean up test user"""
    with app.app_context():
        try:
            # Clean up any existing test data
            existing_user = User.query.filter_by(email=TEST_USER['email']).first()
            
            if existing_user:
                # Delete in correct order to handle foreign key constraints
                Transaction.query.filter_by(user_id=existing_user.id).delete()
                Portfolio.query.filter_by(user_id=existing_user.id).delete()
                User.query.filter_by(id=existing_user.id).delete()
                db_session.commit()
            
            # Create fresh test user
            user = User(
                email=TEST_USER['email'],
                username=TEST_USER['username'],
                initial_balance=TEST_USER['initial_balance'],
                current_balance=TEST_USER['initial_balance']
            )
            db_session.add(user)
            db_session.commit()
            
            yield user
            
            # Cleanup after test
            db_session.begin_nested()
            try:
                # Delete in correct order to handle foreign key constraints
                Transaction.query.filter_by(user_id=user.id).delete()
                Portfolio.query.filter_by(user_id=user.id).delete()
                User.query.filter_by(id=user.id).delete()
                db_session.commit()
            except Exception as e:
                print(f"Cleanup warning: {str(e)}")
                db_session.rollback()
        except Exception as e:
            print(f"Test user fixture error: {str(e)}")
            db_session.rollback()
            raise

@pytest.fixture(scope='session')
def disable_logging():
    """Disable logging during tests"""
    import logging
    logging.getLogger('app').setLevel(logging.ERROR)
    logging.getLogger('apscheduler').setLevel(logging.ERROR)
    
@pytest.fixture(autouse=True)
def cleanup_logs():
    """Clean up log files after tests"""
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    yield
    
    try:
        for log_file in log_dir.glob('*.log'):
            try:
                if log_file.exists():
                    log_file.unlink(missing_ok=True)
            except PermissionError:
                print(f"Warning: Could not delete log file {log_file}")
                pass
    except Exception as e:
        print(f"Warning: Could not cleanup logs: {e}")