import os
from datetime import timedelta, UTC
from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse

# Load environment variables
load_dotenv()

def fix_postgres_url(url):
    """Convert postgres:// to postgresql:// in database URL"""
    if url.startswith('postgres://'):
        url = url.replace('postgres://', 'postgresql://', 1)
    return url

class Config:
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    DEBUG = False
    TESTING = False

    # Database configuration with PostgreSQL dialect fix
    _db_url = os.getenv('DATABASE_URL', 
        '')
    SQLALCHEMY_DATABASE_URI = fix_postgres_url(_db_url)
    if '?' not in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI += '?sslmode=require'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_timeout': 30,
        'pool_recycle': 1800,
        'pool_pre_ping': True,
        'connect_args': {
            'sslmode': 'require'
        }
    }
    
    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Google OAuth configuration
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    
    # CoinGecko API configuration
    COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY')
    COINGECKO_API_URL = 'https://api.coingecko.com/api/v3'
    
    # CORS configuration
    CORS_ORIGINS = ["http://localhost:5173", "https://cryptomock.ie"]
    CORS_HEADERS = ['Content-Type', 'Authorization', 'Access-Control-Allow-Credentials']
    
    # Scheduler configuration
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = UTC
    
    # Price update configuration
    PRICE_UPDATE_INTERVAL = 300  # 5 minutes in seconds
    PRICE_CACHE_DURATION = 60    # 1 minute in seconds
    
    # Trading configuration
    TRADING_FEE_PERCENTAGE = 0.001  # 0.1%
    MIN_TRADE_AMOUNT = 0.00001   # Minimum trade amount
    
    # Logging configuration
    LOG_FILE = "logs/crypto_trading.log"
    LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
    LOG_LEVEL = "INFO"
    LOG_MAX_BYTES = 10240  # 10KB
    LOG_BACKUP_COUNT = 10

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Log SQL queries
    # Use Aiven database for development too
    _db_url = os.getenv('DATABASE_URL', 
        '')
    SQLALCHEMY_DATABASE_URI = fix_postgres_url(_db_url)
    if '?' not in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI += '?sslmode=require'
    CORS_ORIGINS = ["http://localhost:5173", "https://cryptomock.ie"]

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    # Use a separate database for testing
    _db_url = os.getenv('TEST_DATABASE_URL', 
        '')
    SQLALCHEMY_DATABASE_URI = fix_postgres_url(_db_url)
    if '?' not in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI += '?sslmode=require'
    # Disable scheduler for testing
    SCHEDULER_API_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    # Override these with secure values in production
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    # Use Aiven database URL
    _db_url = os.getenv('DATABASE_URL', 
        '')
    SQLALCHEMY_DATABASE_URI = fix_postgres_url(_db_url)
    if '?' not in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI += '?sslmode=require'
    # Stricter CORS settings
    CORS_ORIGINS = ["https://cryptomock.ie"]
    CORS_HEADERS = ['Content-Type', 'Authorization', 'Access-Control-Allow-Credentials']
    # Enhance security in production
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration class based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])