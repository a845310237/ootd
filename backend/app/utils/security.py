"""Security utilities for password hashing and JWT tokens."""
import bcrypt
from datetime import datetime, timedelta
from flask import current_app


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        str: Hashed password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password.

    Args:
        password: Plain text password to verify
        hashed_password: Hashed password to compare against

    Returns:
        bool: True if password matches, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def generate_token(user_id: str, expires_in=None) -> str:
    """
    Generate a JWT access token.

    Args:
        user_id: User ID to include in token
        expires_in: Token expiration time in seconds (default from config)

    Returns:
        str: JWT access token
    """
    from flask_jwt_extended import create_access_token

    if expires_in is None:
        expires_in = current_app.config['JWT_ACCESS_TOKEN_EXPIRES']

    return create_access_token(
        identity=user_id,
        expires_delta=timedelta(seconds=expires_in)
    )


def get_current_user_id() -> str | None:
    """
    Get current user ID from JWT token.

    Returns:
        str | None: Current user ID or None if not authenticated
    """
    from flask_jwt_extended import get_jwt_identity
    return get_jwt_identity()
