"""Outfit API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4
import json

from app.core.database import get_db
from app.models.user import User
from app.models.clothing import Clothing
from app.models.outfit import Outfit, OutfitItem
from app.schemas.outfit import OutfitCreate, OutfitGenerate, OutfitUpdate, OutfitResponse, AIOutfitRequest
from app.api.deps import get_current_user
from app.services.minimax_service import minimax_service

router = APIRouter(prefix="/outfits", tags=["Outfits"])


@router.get("", response_model=List[OutfitResponse])
async def get_outfits(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all outfits for current user.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of outfits
    """
    outfits = db.query(Outfit).filter(
        Outfit.user_id == current_user.id
    ).order_by(Outfit.created_at.desc()).all()

    # Parse JSON fields and load items
    for outfit in outfits:
        if outfit.tips:
            outfit.tips = json.loads(outfit.tips) if isinstance(outfit.tips, str) else outfit.tips

    return outfits


@router.post("/create", response_model=OutfitResponse, status_code=status.HTTP_201_CREATED)
async def create_outfit(
    outfit_in: OutfitCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a DIY outfit.

    Args:
        outfit_in: Outfit creation data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Created outfit
    """
    # Validate clothing items
    clothing_items = db.query(Clothing).filter(
        Clothing.id.in_(outfit_in.clothing_ids),
        Clothing.user_id == current_user.id
    ).all()

    if len(clothing_items) != len(outfit_in.clothing_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Some clothing items not found or don't belong to you"
        )

    # Create outfit
    outfit = Outfit(
        id=str(uuid4()),
        user_id=current_user.id,
        name=outfit_in.name,
        style=outfit_in.style,
        occasion=outfit_in.occasion,
        season=outfit_in.season,
        ai_generated=False
    )

    db.add(outfit)
    db.flush()

    # Add outfit items
    for clothing_id in outfit_in.clothing_ids:
        outfit_item = OutfitItem(
            id=str(uuid4()),
            outfit_id=outfit.id,
            clothing_id=clothing_id
        )
        db.add(outfit_item)

    db.commit()
    db.refresh(outfit)

    return outfit


@router.post("/generate", response_model=OutfitResponse, status_code=status.HTTP_201_CREATED)
async def generate_outfit(
    request: AIOutfitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate an outfit using AI.

    Args:
        request: AI outfit generation request
        current_user: Current authenticated user
        db: Database session

    Returns:
        Generated outfit with AI image
    """
    # Get user's clothing
    all_clothing = db.query(Clothing).filter(
        Clothing.user_id == current_user.id
    ).all()

    if not all_clothing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No clothing items found. Please add clothing to your wardrobe first."
        )

    # Select clothing items (simple logic - select one from each category)
    selected_clothing = []
    categories = set()

    for item in all_clothing:
        item_season = json.loads(item.season) if item.season else []
        if request.season in item_season or not item_season:
            if item.category not in categories:
                selected_clothing.append(item)
                categories.add(item.category)
            if len(selected_clothing) >= 5:
                break

    if not selected_clothing:
        selected_clothing = all_clothing[:3]

    # Build prompt for MiniMax
    user_desc = f"{current_user.height or 'average'}cm height, {current_user.weight or 'average'}kg weight"
    if current_user.body_type:
        user_desc += f", {current_user.body_type} body type"
    if current_user.skin_tone:
        user_desc += f", {current_user.skin_tone} skin tone"

    # If reference image is provided, include user's physical characteristics more prominently
    if request.reference_image:
        user_desc += ". Use the reference image to match the person's facial features, body shape, and overall appearance."

    clothing_desc = [f"{c.name} ({c.category})" for c in selected_clothing]

    prompt = minimax_service.build_outfit_prompt(
        user_description=user_desc,
        clothing_items=clothing_desc,
        style=request.style,
        occasion=request.occasion,
        season=request.season
    )

    # Generate AI image with reference image if provided
    result_url = await minimax_service.generate_outfit_image(
        prompt=prompt,
        reference_image=request.reference_image
    )

    # Create outfit
    outfit = Outfit(
        id=str(uuid4()),
        user_id=current_user.id,
        name=f"AI Generated: {request.style} Outfit",
        style=request.style,
        occasion=request.occasion,
        season=request.season,
        ai_generated=True,
        result_url=result_url,
        prompt=prompt,
        reasoning=f"AI-generated {request.style} outfit for {request.occasion} in {request.season} season." +
                 (" Used your reference image for personalized styling." if request.reference_image else ""),
        tips=json.dumps([
            "This outfit was generated based on your wardrobe",
            "You can customize or regenerate this outfit",
            "Consider the weather and occasion when wearing"
        ] + (["The AI used your reference photo to personalize the look"] if request.reference_image else []))
    )

    db.add(outfit)
    db.flush()

    # Add outfit items
    for clothing in selected_clothing:
        outfit_item = OutfitItem(
            id=str(uuid4()),
            outfit_id=outfit.id,
            clothing_id=clothing.id
        )
        db.add(outfit_item)

    db.commit()
    db.refresh(outfit)

    # Parse JSON fields for response
    if outfit.tips:
        outfit.tips = json.loads(outfit.tips)

    return outfit


@router.get("/{outfit_id}", response_model=OutfitResponse)
async def get_outfit(
    outfit_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific outfit.

    Args:
        outfit_id: Outfit ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Outfit details

    Raises:
        HTTPException: If outfit not found
    """
    outfit = db.query(Outfit).filter(
        Outfit.id == outfit_id,
        Outfit.user_id == current_user.id
    ).first()

    if not outfit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Outfit not found"
        )

    # Parse JSON fields for response
    if outfit.tips:
        outfit.tips = json.loads(outfit.tips) if isinstance(outfit.tips, str) else outfit.tips

    return outfit


@router.delete("/{outfit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_outfit(
    outfit_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an outfit.

    Args:
        outfit_id: Outfit ID
        current_user: Current authenticated user
        db: Database session

    Raises:
        HTTPException: If outfit not found
    """
    outfit = db.query(Outfit).filter(
        Outfit.id == outfit_id,
        Outfit.user_id == current_user.id
    ).first()

    if not outfit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Outfit not found"
        )

    db.delete(outfit)
    db.commit()

    return None
