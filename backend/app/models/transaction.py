from app import db
from datetime import datetime
import enum
from .base import TimestampMixin

class TransactionType(enum.Enum):
    BUY = "buy"
    SELL = "sell"

class Transaction(db.Model, TimestampMixin):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    crypto_symbol = db.Column(db.String(10), nullable=False)
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    fee = db.Column(db.Float, default=0.0)

    # Relationship
    user = db.relationship("User", backref="transactions")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'crypto_symbol': self.crypto_symbol,
            'transaction_type': self.transaction_type.value,
            'quantity': self.quantity,
            'price_per_unit': self.price_per_unit,
            'total_amount': self.total_amount,
            'fee': self.fee,
            'created_at': self.created_at.isoformat()
        }