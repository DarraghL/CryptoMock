from app import db
from datetime import datetime
from sqlalchemy import UniqueConstraint
from .base import TimestampMixin
from decimal import Decimal, ROUND_HALF_UP

class Portfolio(db.Model, TimestampMixin):
    __tablename__ = 'portfolios'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    crypto_symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=0.0)
    average_buy_price = db.Column(db.Float, nullable=False, default=0.0)

    # Relationship
    user = db.relationship("User", backref="portfolios")

    # Unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'crypto_symbol', name='unique_user_crypto'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'crypto_symbol': self.crypto_symbol,
            'quantity': self.quantity,
            'average_buy_price': self.average_buy_price,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    def __init__(self, *args, **kwargs):
        if 'quantity' in kwargs:
            # Convert quantity to Decimal and round to 8 decimal places
            kwargs['quantity'] = float(Decimal(str(kwargs['quantity'])).quantize(
                Decimal('0.00000001'), 
                rounding=ROUND_HALF_UP
            ))
        super().__init__(*args, **kwargs)

    @property
    def formatted_quantity(self):
        """Return quantity formatted to 8 decimal places"""
        return float(Decimal(str(self.quantity)).quantize(
            Decimal('0.00000001'), 
            rounding=ROUND_HALF_UP
        ))