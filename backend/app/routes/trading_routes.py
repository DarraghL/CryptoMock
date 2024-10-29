from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import trading_service, price_service
from app.models.transaction import Transaction
import logging

logger = logging.getLogger(__name__)
trading_bp = Blueprint('trading', __name__, url_prefix='/api/trading')

@trading_bp.route('/recent', methods=['GET'])
@jwt_required()
def get_recent_trades():
    """Get recent trades for the current user"""
    try:
        user_id = get_jwt_identity()
        recent_trades = Transaction.query.filter_by(user_id=user_id)\
            .order_by(Transaction.created_at.desc())\
            .limit(5)\
            .all()
        return jsonify([trade.to_dict() for trade in recent_trades])
    except Exception as e:
        logger.error(f"Error fetching recent trades: {str(e)}")
        return jsonify({'error': 'Failed to fetch recent trades'}), 500

@trading_bp.route('/buy', methods=['POST'])
@jwt_required()
def buy_crypto():
    """Execute a buy order"""
    try:
        # Get and validate input
        data = request.get_json()
        if not all(k in data for k in ['symbol', 'amount']):
            return jsonify({'error': 'Missing required fields'}), 400

        # Get user and parse data
        user_id = get_jwt_identity()
        symbol = data['symbol'].upper()
        amount = float(data['amount'])

        # Execute trade through service
        result = trading_service.execute_buy(user_id, symbol, amount)
        return jsonify(result)

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error executing buy order: {str(e)}")
        return jsonify({'error': 'Failed to execute buy order'}), 500

@trading_bp.route('/sell', methods=['POST'])
@jwt_required()
def sell_crypto():
    """Execute a sell order"""
    try:
        # Get and validate input
        data = request.get_json()
        if not all(k in data for k in ['symbol', 'amount']):
            return jsonify({'error': 'Missing required fields'}), 400

        # Get user and parse data
        user_id = get_jwt_identity()
        symbol = data['symbol'].upper()
        amount = float(data['amount'])

        # Execute trade through service
        result = trading_service.execute_sell(user_id, symbol, amount)
        return jsonify(result)

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error executing sell order: {str(e)}")
        return jsonify({'error': 'Failed to execute sell order'}), 500