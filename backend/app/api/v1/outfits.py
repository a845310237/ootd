"""Outfit API routes for managing outfit combinations."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.outfit import (
    OutfitCreate,
    OutfitUpdate,
    OutfitResponse,
    OutfitDetailResponse,
    OutfitGenerateRequest,
)
from app.services.outfit_service import (
    get_user_outfits,
    create_outfit,
    update_outfit,
    delete_outfit,
    get_outfit_by_id,
    get_outfit_items,
    get_outfit_styles,
)
from app.services.tongyi_service import (
    ZhipuClothingItem,
    ZhipuUser,
    ZhipuRequirements,
    generate_outfit_recommendation,
)

router = APIRouter(prefix="/outfits", tags=["穿搭"])


@router.get("", response_model=List[OutfitResponse])
async def get_outfits(
    style: Optional[str] = Query(None, description="按风格过滤"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's outfit list with optional filtering.

    Args:
        style: Optional style filter
        current_user: Current authenticated user
        db: Database session

    Returns:
        List[OutfitResponse]: List of outfits
    """
    outfits = get_user_outfits(db, current_user.id, style)
    return outfits


@router.get("/styles", response_model=List[str])
async def get_styles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all unique outfit styles for the user.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        List[str]: List of unique style names
    """
    styles = get_outfit_styles(db, current_user.id)
    return styles


@router.post("/generate", response_model=OutfitDetailResponse)
async def generate_ai_outfit(
    requirements: OutfitGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate an AI-powered outfit recommendation based on user requirements.

    Args:
        requirements: Outfit generation requirements (style, occasion, season, optional clothing_ids)
        current_user: Current authenticated user
        db: Database session

    Returns:
        OutfitDetailResponse: AI-generated outfit with selected items and reasoning
    """
    from app.services.wardrobe_service import get_user_clothes, get_clothing_by_id_for_user

    # Get user's clothing items
    # If specific clothing IDs are provided, use only those; otherwise use all clothes
    if requirements.clothing_ids and len(requirements.clothing_ids) > 0:
        # Get only the specified clothing items
        clothes = []
        for clothing_id in requirements.clothing_ids:
            clothing = get_clothing_by_id_for_user(db, current_user.id, clothing_id)
            if clothing:
                clothes.append(clothing)

        if not clothes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="选择的衣物不存在或无权访问"
            )
    else:
        # Get all user's clothing items
        clothes = get_user_clothes(db, current_user.id)

        if not clothes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="请先添加衣物到衣柜"
            )

    # Build request for Zhipu AI service
    clothing_items = [
        ZhipuClothingItem(
            id=c.id,
            name=c.name,
            category=c.category,
            color=json.loads(c.color) if c.color else [],
            style=json.loads(c.style) if c.style else [],
            season=json.loads(c.season) if c.season else [],
            imageUrl=c.image_url
        ) for c in clothes
    ]

    user_info = ZhipuUser(
        height=current_user.height or 170,
        weight=current_user.weight or 65,
        body_type=current_user.body_type or "标准",
        skin_tone=current_user.skin_tone or "中性"
    )

    zhipu_req = ZhipuRequirements(
        style=requirements.style,
        occasion=requirements.occasion,
        season=requirements.season
    )

    # Call Zhipu AI service
    try:
        result = generate_outfit_recommendation(
            user_info,
            clothing_items,
            zhipu_req
        )

        # Create outfit with AI recommendations
        outfit_create = OutfitCreate(
            name=f"AI生成: {requirements.style}穿搭",
            style=requirements.style,
            occasion=requirements.occasion,
            season=requirements.season,
            reasoning=result.reasoning,
            tips=json.dumps(result.tips, ensure_ascii=False),
            clothing_ids=result.selected_items
        )

        outfit = create_outfit(db, current_user.id, outfit_create, ai_generated=True)

        # Load items for response
        items = get_outfit_items(db, outfit.id)
        outfit.items = items

        return outfit

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI生成失败: {str(e)}"
        )


@router.post("", response_model=OutfitDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_diy_outfit(
    outfit_data: OutfitCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a manual DIY outfit.

    Args:
        outfit_data: Outfit creation data
        current_user: Current authenticated user
        db: Database session

    Returns:
        OutfitDetailResponse: Created outfit with items
    """
    try:
        outfit = create_outfit(db, current_user.id, outfit_data, ai_generated=False)

        # Load items for response
        items = get_outfit_items(db, outfit.id)
        outfit.items = items

        return outfit
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{outfit_id}", response_model=OutfitDetailResponse)
async def get_outfit(
    outfit_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get an outfit by ID.

    Args:
        outfit_id: Outfit ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        OutfitDetailResponse: Outfit with items

    Raises:
        HTTPException: If outfit not found or access denied
    """
    outfit = get_outfit_by_id(db, outfit_id)

    if not outfit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="穿搭不存在"
        )

    if outfit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看此穿搭"
        )

    # Load items for response
    items = get_outfit_items(db, outfit.id)
    outfit.items = items

    return outfit


@router.put("/{outfit_id}", response_model=OutfitDetailResponse)
async def update_outfit_endpoint(
    outfit_id: str,
    outfit_data: OutfitUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an outfit.

    Args:
        outfit_id: ID of the outfit to update
        outfit_data: Outfit update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        OutfitDetailResponse: Updated outfit with items

    Raises:
        HTTPException: If outfit not found or access denied
    """
    try:
        outfit = update_outfit(db, outfit_id, current_user.id, outfit_data)

        # Load items for response
        items = get_outfit_items(db, outfit.id)
        outfit.items = items

        return outfit
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "不存在" in str(e) else status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.delete("/{outfit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_outfit_endpoint(
    outfit_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an outfit.

    Args:
        outfit_id: ID of the outfit to delete
        current_user: Current authenticated user
        db: Database session

    Raises:
        HTTPException: If outfit not found or access denied
    """
    try:
        delete_outfit(db, outfit_id, current_user.id)
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "不存在" in str(e) else status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
