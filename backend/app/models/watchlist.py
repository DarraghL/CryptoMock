from app import db
from datetime import datetime
from sqlalchemy import UniqueConstraint
from .base import TimestampMixin

class WatchlistItem(db.Model, TimestampMixin):
    __tablename__ = 'watchlist_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    crypto_symbol = db.Column(db.String(10), nullable=False)
    notes = db.Column(db.String(200))

    # Relationship
    user = db.relationship("User", backref="watchlist_items")

    __table_args__ = (
        UniqueConstraint('user_id', 'crypto_symbol', name='unique_user_watchlist_crypto'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'crypto_symbol': self.crypto_symbol,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }