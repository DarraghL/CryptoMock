from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from flask_cors import cross_origin
from datetime import datetime, timedelta
import requests
from app import db
from app.models.user import User
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/google', methods=['POST', 'OPTIONS'])
@cross_origin()
def google_auth():
    """Handle Google authentication"""
    # Handle preflight request
    if request.method == 'OPTIONS':
        response = current_app.make_default_options_response()
        return response

    try:
        token = request.json.get('token')
        if not token:
            logger.error("No token provided in request")
            return jsonify({'error': 'No token provided'}), 400

        logger.debug("Received token, verifying with Google...")

        # Verify token with Google
        google_response = requests.get(
            f'https://oauth2.googleapis.com/tokeninfo?id_token={token}'
        )

        if not google_response.ok:
            logger.error(f"Google verification failed: {google_response.text}")
            return jsonify({'error': 'Failed to verify Google token'}), 401

        google_data = google_response.json()
        logger.debug(f"Google verification successful for email: {google_data.get('email')}")

        try:
            # Get or create user within a transaction
            with db.session.begin_nested():
                user = User.query.filter_by(email=google_data['email']).first()
                if not user:
                    logger.info(f"Creating new user for email: {google_data['email']}")
                    user = User(
                        email=google_data['email'],
                        username=google_data.get('given_name', 'User'),
                        picture=google_data.get('picture'),
                        initial_balance=100000.0,
                        current_balance=100000.0
                    )
                    db.session.add(user)
                else:
                    logger.info(f"Existing user found for email: {google_data['email']}")

                # Update last login
                user.last_login = datetime.utcnow()

            # Commit the transaction
            db.session.commit()

            # Create JWT tokens
            access_token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(hours=1)
            )
            refresh_token = create_refresh_token(
                identity=user.id,
                expires_delta=timedelta(days=30)
            )

            logger.info(f"Authentication successful for user: {user.email}")
            return jsonify({
                'message': 'Authentication successful',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user.to_dict()
            }), 200

        except Exception as db_error:
            logger.error(f"Database error: {str(db_error)}")
            db.session.rollback()
            return jsonify({'error': 'Database error occurred'}), 500

    except requests.RequestException as e:
        logger.error(f"Google API error: {str(e)}")
        return jsonify({'error': 'Failed to verify with Google'}), 503
    except Exception as e:
        logger.error(f"Unexpected error during authentication: {str(e)}")
        return jsonify({'error': 'Authentication failed'}), 500

@auth_bp.route('/refresh', methods=['POST', 'OPTIONS'])
@cross_origin()
@jwt_required(refresh=True)
def refresh_token():
    """Refresh access token"""
    if request.method == 'OPTIONS':
        response = current_app.make_default_options_response()
        return response

    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        access_token = create_access_token(
            identity=current_user_id,
            expires_delta=timedelta(hours=1)
        )
        logger.info(f"Token refreshed for user ID: {current_user_id}")
        return jsonify({
            'access_token': access_token,
            'message': 'Token refreshed successfully'
        }), 200
    except Exception as e:
        logger.error(f"Error refreshing token: {str(e)}")
        return jsonify({'error': 'Token refresh failed'}), 500

@auth_bp.route('/verify', methods=['GET', 'OPTIONS'])  # Fixed route path
@cross_origin()
@jwt_required()
def verify_token():
    """Verify JWT token and return user data"""
    if request.method == 'OPTIONS':
        response = current_app.make_default_options_response()
        return response

    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify({
            'user': user.to_dict(),
            'verified': True
        }), 200
        
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return jsonify({'error': 'Token verification failed'}), 401

# Error handlers
@auth_bp.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

@auth_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500