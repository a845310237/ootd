"""User service for user profile management."""
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.user import User
from app.schemas.user import UserUpdate


def get_user(db: Session, user_id: str) -> Optional[User]:
    """
    Get a user by ID.

    Args:
        db: Database session
        user_id: User's ID

    Returns:
        Optional[User]: User object if found, None otherwise
    """
    return db.query(User).filter(User.id == user_id).first()


def update_user_profile(db: Session, user_id: str, profile_data: UserUpdate) -> User:
    """
    Update user profile information.

    Args:
        db: Database session
        user_id: User's ID
        profile_data: Profile update data

    Returns:
        User: Updated user object

    Raises:
        ValueError: If user not found
    """
    user = get_user(db, user_id)
    if not user:
        raise ValueError("用户不存在")

    # Update only provided fields
    update_data = profile_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Get all users with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List[User]: List of user objects
    """
    return db.query(User).offset(skip).limit(limit).all()
