from app import db
from datetime import datetime
from .base import TimestampMixin

class User(db.Model, TimestampMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    picture = db.Column(db.String(255), nullable=True)
    initial_balance = db.Column(db.Float, default=100000.0)
    current_balance = db.Column(db.Float, default=100000.0)
    last_login = db.Column(db.DateTime, nullable=True)
    # TimestampMixin adds created_at and updated_at

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'picture': self.picture,
            'current_balance': self.current_balance,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }