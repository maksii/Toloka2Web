"""User model for authentication and authorization."""
from flask_login import UserMixin
from .base import db
from flask_bcrypt import Bcrypt

bcrypt: Bcrypt = Bcrypt()  # This will be initialized in the app.py

class User(UserMixin, db.Model):
    """User model representing application users.
    
    Attributes:
        id: The primary key of the user
        username: Unique username for the user
        password_hash: Hashed password string
        roles: Comma-separated string of user roles
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    roles = db.Column(db.String(80), nullable=False)
    
    # Relationships
    settings = db.relationship('UserSettings', backref='user', lazy=True)
    releases = db.relationship('Releases', backref='user', lazy=True)

    def set_password(self, password: str) -> None:
        """Hash and set the user's password.
        
        Args:
            password: The plain text password to hash and store
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Verify if the provided password matches the stored hash.
        
        Args:
            password: The plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.check_password_hash(self.password_hash, password)