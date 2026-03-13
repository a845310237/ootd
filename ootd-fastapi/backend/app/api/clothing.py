"""Clothing API routes."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4
import json

from app.core.database import get_db
from app.models.user import User
from app.models.clothing import Clothing
from app.schemas.clothing import ClothingCreate, ClothingUpdate, ClothingResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/clothing", tags=["Clothing"])


@router.get("", response_model=List[ClothingResponse])
async def get_clothing(
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search by name"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all clothing items for current user.

    Args:
        category: Optional category filter
        search: Optional search query
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of clothing items
    """
    query = db.query(Clothing).filter(Clothing.user_id == current_user.id)

    if category:
        query = query.filter(Clothing.category == category)

    if search:
        query = query.filter(Clothing.name.contains(search))

    clothing = query.order_by(Clothing.created_at.desc()).all()

    # Parse JSON fields
    for item in clothing:
        if item.color:
            item.color = json.loads(item.color) if isinstance(item.color, str) else item.color
        if item.style:
            item.style = json.loads(item.style) if isinstance(item.style, str) else item.style
        if item.season:
            item.season = json.loads(item.season) if isinstance(item.season, str) else item.season

    return clothing


@router.post("", response_model=ClothingResponse, status_code=status.HTTP_201_CREATED)
async def create_clothing(
    clothing_in: ClothingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new clothing item.

    Args:
        clothing_in: Clothing creation data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Created clothing item
    """
    clothing = Clothing(
        id=str(uuid4()),
        user_id=current_user.id,
        name=clothing_in.name,
        category=clothing_in.category,
        color=json.dumps(clothing_in.color) if clothing_in.color else None,
        style=json.dumps(clothing_in.style) if clothing_in.style else None,
        season=json.dumps(clothing_in.season) if clothing_in.season else None,
        brand=clothing_in.brand,
        size=clothing_in.size,
        material=clothing_in.material,
        image_url=clothing_in.image_url
    )

    db.add(clothing)
    db.commit()
    db.refresh(clothing)

    # Parse JSON fields for response
    if clothing.color:
        clothing.color = json.loads(clothing.color)
    if clothing.style:
        clothing.style = json.loads(clothing.style)
    if clothing.season:
        clothing.season = json.loads(clothing.season)

    return clothing


@router.get("/{clothing_id}", response_model=ClothingResponse)
async def get_clothing_item(
    clothing_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific clothing item.

    Args:
        clothing_id: Clothing item ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Clothing item

    Raises:
        HTTPException: If clothing not found
    """
    clothing = db.query(Clothing).filter(
        Clothing.id == clothing_id,
        Clothing.user_id == current_user.id
    ).first()

    if not clothing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clothing item not found"
        )

    # Parse JSON fields for response
    if clothing.color:
        clothing.color = json.loads(clothing.color)
    if clothing.style:
        clothing.style = json.loads(clothing.style)
    if clothing.season:
        clothing.season = json.loads(clothing.season)

    return clothing


@router.put("/{clothing_id}", response_model=ClothingResponse)
async def update_clothing(
    clothing_id: str,
    clothing_in: ClothingUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a clothing item.

    Args:
        clothing_id: Clothing item ID
        clothing_in: Clothing update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated clothing item

    Raises:
        HTTPException: If clothing not found
    """
    clothing = db.query(Clothing).filter(
        Clothing.id == clothing_id,
        Clothing.user_id == current_user.id
    ).first()

    if not clothing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clothing item not found"
        )

    # Update fields
    update_data = clothing_in.model_dump(exclude_unset=True, exclude_none=True)

    for field, value in update_data.items():
        if field in ["color", "style", "season"] and isinstance(value, list):
            setattr(clothing, field, json.dumps(value))
        else:
            setattr(clothing, field, value)

    db.commit()
    db.refresh(clothing)

    # Parse JSON fields for response
    if clothing.color:
        clothing.color = json.loads(clothing.color)
    if clothing.style:
        clothing.style = json.loads(clothing.style)
    if clothing.season:
        clothing.season = json.loads(clothing.season)

    return clothing


@router.delete("/{clothing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_clothing(
    clothing_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a clothing item.

    Args:
        clothing_id: Clothing item ID
        current_user: Current authenticated user
        db: Database session

    Raises:
        HTTPException: If clothing not found
    """
    clothing = db.query(Clothing).filter(
        Clothing.id == clothing_id,
        Clothing.user_id == current_user.id
    ).first()

    if not clothing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clothing item not found"
        )

    db.delete(clothing)
    db.commit()

    return None
