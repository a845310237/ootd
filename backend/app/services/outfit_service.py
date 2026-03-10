"""Outfit service for managing outfit combinations."""
from sqlalchemy.orm import Session
from typing import Optional, List
import json
import uuid
from app.models.outfit import Outfit
from app.models.outfit_item import OutfitItem
from app.models.clothing import Clothing
from app.schemas.outfit import OutfitCreate, OutfitUpdate


def get_outfit_by_id(db: Session, outfit_id: str) -> Optional[Outfit]:
    """
    Get an outfit by ID.

    Args:
        db: Database session
        outfit_id: Outfit ID

    Returns:
        Optional[Outfit]: Outfit object if found, None otherwise
    """
    return db.query(Outfit).filter(Outfit.id == outfit_id).first()


def get_user_outfits(
    db: Session,
    user_id: str,
    style: Optional[str] = None
) -> List[Outfit]:
    """
    Get all outfits for a user with optional filtering.

    Args:
        db: Database session
        user_id: User's ID
        style: Optional style filter

    Returns:
        List[Outfit]: List of outfit objects
    """
    query = db.query(Outfit).filter(Outfit.user_id == user_id)

    if style:
        query = query.filter(Outfit.style == style)

    return query.order_by(Outfit.created_at.desc()).all()


def create_outfit(
    db: Session,
    user_id: str,
    outfit_data: OutfitCreate,
    ai_generated: bool = False
) -> Outfit:
    """
    Create a new outfit.

    Args:
        db: Database session
        user_id: User's ID
        outfit_data: Outfit creation data
        ai_generated: Whether this is an AI-generated outfit

    Returns:
        Outfit: Created outfit object

    Raises:
        ValueError: If clothing items not found or don't belong to user
    """
    # Verify all clothing items exist and belong to user
    clothing_items = db.query(Clothing).filter(
        Clothing.id.in_(outfit_data.clothing_ids),
        Clothing.user_id == user_id
    ).all()

    if len(clothing_items) != len(outfit_data.clothing_ids):
        raise ValueError("部分衣物不存在或无权访问")

    # Create outfit
    outfit_dict = outfit_data.dict(exclude={"clothing_ids"})

    db_outfit = Outfit(
        id=str(uuid.uuid4()),
        user_id=user_id,
        ai_generated=ai_generated,
        **outfit_dict
    )

    db.add(db_outfit)
    db.flush()  # Flush to get the outfit ID

    # Create outfit items
    for clothing_id in outfit_data.clothing_ids:
        outfit_item = OutfitItem(
            id=str(uuid.uuid4()),
            outfit_id=db_outfit.id,
            clothing_id=clothing_id
        )
        db.add(outfit_item)

    db.commit()
    db.refresh(db_outfit)

    return db_outfit


def update_outfit(
    db: Session,
    outfit_id: str,
    user_id: str,
    outfit_data: OutfitUpdate
) -> Outfit:
    """
    Update an outfit.

    Args:
        db: Database session
        outfit_id: Outfit ID
        user_id: User's ID (for ownership verification)
        outfit_data: Outfit update data

    Returns:
        Outfit: Updated outfit object

    Raises:
        ValueError: If outfit not found or doesn't belong to user
    """
    outfit = get_outfit_by_id(db, outfit_id)

    if not outfit:
        raise ValueError("穿搭不存在")

    if outfit.user_id != user_id:
        raise ValueError("无权修改此穿搭")

    # Update only provided fields
    update_data = outfit_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(outfit, field, value)

    db.commit()
    db.refresh(outfit)

    return outfit


def delete_outfit(db: Session, outfit_id: str, user_id: str) -> None:
    """
    Delete an outfit.

    Args:
        db: Database session
        outfit_id: Outfit ID
        user_id: User's ID (for ownership verification)

    Raises:
        ValueError: If outfit not found or doesn't belong to user
    """
    outfit = get_outfit_by_id(db, outfit_id)

    if not outfit:
        raise ValueError("穿搭不存在")

    if outfit.user_id != user_id:
        raise ValueError("无权删除此穿搭")

    db.delete(outfit)
    db.commit()


def get_outfit_items(db: Session, outfit_id: str) -> List[OutfitItem]:
    """
    Get all items in an outfit.

    Args:
        db: Database session
        outfit_id: Outfit ID

    Returns:
        List[OutfitItem]: List of outfit items
    """
    return db.query(OutfitItem).filter(OutfitItem.outfit_id == outfit_id).all()


def get_outfit_styles(db: Session, user_id: str) -> List[str]:
    """
    Get all unique styles for a user's outfits.

    Args:
        db: Database session
        user_id: User's ID

    Returns:
        List[str]: List of unique style names
    """
    styles = db.query(Outfit.style).filter(
        Outfit.user_id == user_id
    ).distinct().all()

    return [style[0] for style in styles]
