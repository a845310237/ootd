"""Outfit schemas for request and response validation."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import json


class OutfitItemBase(BaseModel):
    """Base outfit item schema."""

    clothing_id: str


class OutfitItemCreate(OutfitItemBase):
    """Schema for adding an item to an outfit."""

    pass


class OutfitItemResponse(BaseModel):
    """Schema for outfit item response."""

    id: str
    outfit_id: str
    clothing_id: str
    created_at: datetime

    class Config:
        orm_mode = True


class OutfitBase(BaseModel):
    """Base outfit schema with common fields."""

    name: str = Field(..., min_length=1, max_length=255)
    style: str = Field(..., min_length=1, max_length=100)
    occasion: Optional[str] = Field(None, max_length=100)
    season: Optional[str] = Field(None, max_length=50)


class OutfitCreate(OutfitBase):
    """Schema for creating a new outfit."""

    reasoning: Optional[str] = None
    tips: Optional[str] = Field(None, description="JSON array of tips")
    clothing_ids: List[str] = Field(..., min_length=1, description="List of clothing item IDs")


class OutfitUpdate(BaseModel):
    """Schema for updating an outfit."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    style: Optional[str] = Field(None, min_length=1, max_length=100)
    occasion: Optional[str] = Field(None, max_length=100)
    season: Optional[str] = Field(None, max_length=50)
    reasoning: Optional[str] = None
    tips: Optional[str] = None


class OutfitGenerateRequest(BaseModel):
    """Schema for AI outfit generation request."""

    style: str = Field(..., min_length=1, max_length=100, description="Desired style")
    occasion: str = Field(..., min_length=1, max_length=100, description="Occasion")
    season: str = Field(..., min_length=1, max_length=50, description="Season")
    clothing_ids: Optional[List[str]] = Field(None, description="Optional list of specific clothing item IDs to use")


class OutfitResponse(OutfitBase):
    """Schema for outfit response."""

    id: str
    user_id: str
    ai_generated: bool
    result_url: Optional[str] = None
    prompt: Optional[str] = None
    reasoning: Optional[str] = None
    tips: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

    @property
    def tips_list(self) -> List[str]:
        """Parse tips JSON string to list."""
        if self.tips:
            try:
                return json.loads(self.tips)
            except (json.JSONDecodeError, TypeError):
                return []
        return []


class OutfitDetailResponse(OutfitResponse):
    """Detailed outfit response with items."""

    items: List[OutfitItemResponse] = []
