from flask import Blueprint

# Create blueprints
market_bp = Blueprint('market', __name__, url_prefix='/api/market')
trading_bp = Blueprint('trading', __name__, url_prefix='/api/trading')
portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/api/portfolio')
user_bp = Blueprint('user', __name__, url_prefix='/api/user')

# Import routes after creating blueprints
from .market_routes import *
from .trading_routes import *
from .portfolio_routes import *
from .user_routes import *

# Export blueprints
__all__ = [
    'market_bp',
    'trading_bp',
    'portfolio_bp',
    'user_bp'
]