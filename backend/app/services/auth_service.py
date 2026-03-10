"""Authentication service for user registration, login, and token management."""
from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get a user by email address.

    Args:
        db: Database session
        email: User's email address

    Returns:
        Optional[User]: User object if found, None otherwise
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """
    Get a user by ID.

    Args:
        db: Database session
        user_id: User's ID

    Returns:
        Optional[User]: User object if found, None otherwise
    """
    return db.query(User).filter(User.id == user_id).first()


def register_user(db: Session, user_data: UserCreate) -> User:
    """
    Register a new user.

    Args:
        db: Database session
        user_data: User registration data

    Returns:
        User: Created user object

    Raises:
        ValueError: If email already exists
    """
    # Check if user already exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise ValueError("该邮箱已被注册")

    # Create new user
    import uuid
    db_user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        name=user_data.name,
        password=get_password_hash(user_data.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user with email and password.

    Args:
        db: Database session
        email: User's email address
        password: Plain text password

    Returns:
        Optional[User]: User object if authentication successful, None otherwise
    """
    user = get_user_by_email(db, email)
    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


def create_user_token(user: User) -> str:
    """
    Create a JWT access token for a user.

    Args:
        user: User object

    Returns:
        str: JWT access token
    """
    return create_access_token(data={"sub": user.email})
