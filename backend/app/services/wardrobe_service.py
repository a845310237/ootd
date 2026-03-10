"""Wardrobe (clothing) service for managing user's clothing items."""
from sqlalchemy.orm import Session
from typing import Optional, List
import json
import uuid
from app.models.clothing import Clothing
from app.schemas.clothing import ClothingCreate, ClothingUpdate


def get_clothing_by_id(db: Session, clothing_id: str) -> Optional[Clothing]:
    """
    Get a clothing item by ID.

    Args:
        db: Database session
        clothing_id: Clothing item ID

    Returns:
        Optional[Clothing]: Clothing object if found, None otherwise
    """
    return db.query(Clothing).filter(Clothing.id == clothing_id).first()


def get_clothing_by_id_for_user(db: Session, user_id: str, clothing_id: str) -> Optional[Clothing]:
    """
    Get a clothing item by ID with user ownership verification.

    Args:
        db: Database session
        user_id: User's ID
        clothing_id: Clothing item ID

    Returns:
        Optional[Clothing]: Clothing object if found and belongs to user, None otherwise
    """
    return db.query(Clothing).filter(
        Clothing.id == clothing_id,
        Clothing.user_id == user_id
    ).first()


def get_user_clothes(
    db: Session,
    user_id: str,
    category: Optional[str] = None,
    search: Optional[str] = None
) -> List[Clothing]:
    """
    Get all clothing items for a user with optional filtering.

    Args:
        db: Database session
        user_id: User's ID
        category: Optional category filter
        search: Optional search term for name

    Returns:
        List[Clothing]: List of clothing items
    """
    query = db.query(Clothing).filter(Clothing.user_id == user_id)

    if category:
        query = query.filter(Clothing.category == category)

    if search:
        query = query.filter(Clothing.name.contains(search))

    return query.order_by(Clothing.created_at.desc()).all()


def create_clothing(db: Session, user_id: str, clothing_data: ClothingCreate) -> Clothing:
    """
    Create a new clothing item.

    Args:
        db: Database session
        user_id: User's ID
        clothing_data: Clothing creation data

    Returns:
        Clothing: Created clothing object
    """
    # Convert lists to JSON strings if provided
    clothing_dict = clothing_data.dict()

    db_clothing = Clothing(
        id=str(uuid.uuid4()),
        user_id=user_id,
        **clothing_dict
    )

    db.add(db_clothing)
    db.commit()
    db.refresh(db_clothing)

    return db_clothing


def update_clothing(
    db: Session,
    clothing_id: str,
    user_id: str,
    clothing_data: ClothingUpdate
) -> Clothing:
    """
    Update a clothing item.

    Args:
        db: Database session
        clothing_id: Clothing item ID
        user_id: User's ID (for ownership verification)
        clothing_data: Clothing update data

    Returns:
        Clothing: Updated clothing object

    Raises:
        ValueError: If clothing not found or doesn't belong to user
    """
    clothing = get_clothing_by_id(db, clothing_id)

    if not clothing:
        raise ValueError("衣物不存在")

    if clothing.user_id != user_id:
        raise ValueError("无权修改此衣物")

    # Update only provided fields
    update_data = clothing_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(clothing, field, value)

    db.commit()
    db.refresh(clothing)

    return clothing


def delete_clothing(db: Session, clothing_id: str, user_id: str) -> None:
    """
    Delete a clothing item.

    Args:
        db: Database session
        clothing_id: Clothing item ID
        user_id: User's ID (for ownership verification)

    Raises:
        ValueError: If clothing not found or doesn't belong to user
    """
    clothing = get_clothing_by_id(db, clothing_id)

    if not clothing:
        raise ValueError("衣物不存在")

    if clothing.user_id != user_id:
        raise ValueError("无权删除此衣物")

    db.delete(clothing)
    db.commit()


def get_clothing_categories(db: Session, user_id: str) -> List[str]:
    """
    Get all unique categories for a user's clothing.

    Args:
        db: Database session
        user_id: User's ID

    Returns:
        List[str]: List of unique category names
    """
    categories = db.query(Clothing.category).filter(
        Clothing.user_id == user_id
    ).distinct().all()

    return [category[0] for category in categories]
