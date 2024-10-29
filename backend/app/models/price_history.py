from app import db
from datetime import datetime
from sqlalchemy import Index
from .base import TimestampMixin

class PriceHistory(db.Model, TimestampMixin):
    __tablename__ = 'price_history'

    id = db.Column(db.Integer, primary_key=True)
    crypto_symbol = db.Column(db.String(10), nullable=False)
    price_usd = db.Column(db.Float, nullable=False)
    volume_24h = db.Column(db.Float)
    market_cap = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_crypto_timestamp', 'crypto_symbol', 'timestamp'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'crypto_symbol': self.crypto_symbol,
            'price_usd': self.price_usd,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'volume_24h': self.volume_24h,
            'market_cap': self.market_cap
        }