from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.portfolio import Portfolio
from app.services.price_service import PriceService

portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/api/portfolio')
price_service = PriceService()

@portfolio_bp.route('/balance', methods=['GET'])
@jwt_required()
def get_balance():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # Get current prices for all cryptocurrencies
        current_prices = price_service.get_all_prices()
        
        # Calculate crypto balance using current market prices
        crypto_balance = 0
        for holding in user.portfolios:
            if holding.crypto_symbol in current_prices:
                current_price = current_prices[holding.crypto_symbol]['price']
                crypto_balance += holding.quantity * current_price
        
        total_balance = user.current_balance + crypto_balance
        
        return jsonify({
            'cash_balance': user.current_balance,
            'crypto_balance': crypto_balance,
            'total_balance': total_balance,
            'last_updated': current_prices.get('timestamp', None)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/holdings', methods=['GET'])
@jwt_required()
def get_holdings():
    try:
        current_user_id = get_jwt_identity()
        holdings = Portfolio.query.filter_by(user_id=current_user_id).all()
        
        # Get current prices for all cryptocurrencies
        current_prices = price_service.get_all_prices()
        
        holdings_data = []
        for holding in holdings:
            holding_dict = holding.to_dict()
            if holding.crypto_symbol in current_prices:
                current_price = current_prices[holding.crypto_symbol]['price']
                holding_dict['current_price'] = current_price
                holding_dict['current_value'] = holding.quantity * current_price
                holding_dict['profit_loss'] = (current_price - holding.average_buy_price) * holding.quantity
            holdings_data.append(holding_dict)
        
        return jsonify({
            'holdings': holdings_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500