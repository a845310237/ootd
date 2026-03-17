"""Outfit schemas for request and response validation."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class OutfitItemBase(BaseModel):
    """Base outfit item schema."""

    id: str
    clothing_id: str


class OutfitItemResponse(OutfitItemBase):
    """Outfit item response schema."""

    class Config:
        orm_mode = True


class OutfitBase(BaseModel):
    """Base outfit schema."""

    name: str = Field(..., min_length=1, max_length=255)
    style: str = Field(..., min_length=1, max_length=100)
    occasion: Optional[str] = None
    season: Optional[str] = None


class OutfitCreate(OutfitBase):
    """Outfit creation schema for DIY."""

    clothing_ids: List[str] = Field(..., min_items=1)


class OutfitGenerate(OutfitBase):
    """Outfit generation schema for AI."""

    prompt: Optional[str] = None


class OutfitUpdate(OutfitBase):
    """Outfit update schema."""

    name: Optional[str] = None
    style: Optional[str] = None
    reasoning: Optional[str] = None
    tips: Optional[List[str]] = None


class OutfitResponse(OutfitBase):
    """Outfit response schema."""

    id: str
    user_id: str
    ai_generated: bool
    result_url: Optional[str] = None
    prompt: Optional[str] = None
    reasoning: Optional[str] = None
    tips: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime
    items: List[OutfitItemResponse] = []

    class Config:
        orm_mode = True


class AIOutfitRequest(BaseModel):
    """AI outfit generation request schema."""

    style: str
    occasion: str
    season: str
    reference_image: Optional[str] = None  # URL of reference image (user uploaded or avatar)
    custom_description: Optional[str] = None  # Custom description for the outfit
