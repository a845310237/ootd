"""Wardrobe (clothing) API routes for managing user's clothing items."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.clothing import ClothingCreate, ClothingResponse, ClothingUpdate
from app.services.wardrobe_service import (
    get_user_clothes,
    create_clothing,
    update_clothing,
    delete_clothing,
    get_clothing_by_id,
    get_clothing_categories,
)

router = APIRouter(prefix="/wardrobe", tags=["衣柜"])


@router.get("", response_model=List[ClothingResponse])
async def get_wardrobe(
    category: Optional[str] = Query(None, description="按类别过滤"),
    search: Optional[str] = Query(None, description="搜索名称"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's clothing list with optional filtering.

    Args:
        category: Optional category filter
        search: Optional search term for clothing name
        current_user: Current authenticated user
        db: Database session

    Returns:
        List[ClothingResponse]: List of clothing items
    """
    clothes = get_user_clothes(db, current_user.id, category, search)
    return clothes


@router.get("/categories", response_model=List[str])
async def get_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all unique clothing categories for the user.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        List[str]: List of unique category names
    """
    categories = get_clothing_categories(db, current_user.id)
    return categories


@router.post("", response_model=ClothingResponse, status_code=status.HTTP_201_CREATED)
async def add_clothing(
    clothing_data: ClothingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a new clothing item to the user's wardrobe.

    Args:
        clothing_data: Clothing creation data
        current_user: Current authenticated user
        db: Database session

    Returns:
        ClothingResponse: Created clothing item
    """
    clothing = create_clothing(db, current_user.id, clothing_data)
    return clothing


@router.put("/{clothing_id}", response_model=ClothingResponse)
async def update_clothing_item(
    clothing_id: str,
    clothing_data: ClothingUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a clothing item.

    Args:
        clothing_id: ID of the clothing item to update
        clothing_data: Clothing update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        ClothingResponse: Updated clothing item

    Raises:
        HTTPException: If clothing not found or access denied
    """
    try:
        clothing = update_clothing(db, clothing_id, current_user.id, clothing_data)
        return clothing
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "不存在" in str(e) else status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.delete("/{clothing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_clothing_item(
    clothing_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a clothing item.

    Args:
        clothing_id: ID of the clothing item to delete
        current_user: Current authenticated user
        db: Database session

    Raises:
        HTTPException: If clothing not found or access denied
    """
    try:
        delete_clothing(db, clothing_id, current_user.id)
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "不存在" in str(e) else status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
