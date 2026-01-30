"""Revoked Token model for persistent JWT blocklist."""
from datetime import datetime, timezone
from .base import db


class RevokedToken(db.Model):
    """Model for storing revoked JWT tokens.
    
    This provides a persistent token blocklist that survives application restarts.
    Tokens are stored by their JTI (JWT ID) and can be checked during authentication.
    
    Attributes:
        id: Primary key
        jti: JWT ID (unique identifier for the token)
        revoked_at: Timestamp when the token was revoked
    """
    __tablename__ = 'revoked_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), unique=True, nullable=False, index=True)
    revoked_at = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    def __repr__(self) -> str:
        """String representation of the RevokedToken."""
        return f'<RevokedToken {self.jti}>'
    
    @classmethod
    def is_token_revoked(cls, jti: str) -> bool:
        """Check if a token has been revoked.
        
        Args:
            jti: The JWT ID to check
            
        Returns:
            True if token is revoked, False otherwise
        """
        return cls.query.filter_by(jti=jti).first() is not None
    
    @classmethod
    def revoke_token(cls, jti: str) -> 'RevokedToken':
        """Add a token to the blocklist.
        
        Args:
            jti: The JWT ID to revoke
            
        Returns:
            The created RevokedToken instance
        """
        revoked = cls(jti=jti)
        db.session.add(revoked)
        db.session.commit()
        return revoked
    
    @classmethod
    def cleanup_expired_tokens(cls, max_age_days: int = 30) -> int:
        """Remove old revoked tokens from the database.
        
        Tokens older than max_age_days are removed since they would have
        expired anyway.
        
        Args:
            max_age_days: Maximum age of tokens to keep
            
        Returns:
            Number of tokens removed
        """
        from datetime import timedelta
        
        cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
        result = cls.query.filter(cls.revoked_at < cutoff).delete()
        db.session.commit()
        return result
