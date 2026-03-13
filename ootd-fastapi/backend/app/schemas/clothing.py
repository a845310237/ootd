"""Clothing schemas for request and response validation."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ClothingBase(BaseModel):
    """Base clothing schema."""

    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)
    color: List[str] = []
    style: List[str] = []
    season: List[str] = []


class ClothingCreate(ClothingBase):
    """Clothing creation schema."""

    brand: Optional[str] = None
    size: Optional[str] = None
    material: Optional[str] = None
    image_url: str = Field(..., min_length=1, max_length=500)


class ClothingUpdate(ClothingBase):
    """Clothing update schema."""

    brand: Optional[str] = None
    size: Optional[str] = None
    material: Optional[str] = None
    image_url: Optional[str] = None


class ClothingResponse(ClothingBase):
    """Clothing response schema."""

    id: str
    user_id: str
    brand: Optional[str] = None
    size: Optional[str] = None
    material: Optional[str] = None
    image_url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
