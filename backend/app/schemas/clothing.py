"""Clothing schemas for request and response validation."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import json


class ClothingBase(BaseModel):
    """Base clothing schema with common fields."""

    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = Field(None, description="JSON array of colors")
    style: Optional[str] = Field(None, description="JSON array of styles")
    season: Optional[str] = Field(None, description="JSON array of seasons")
    brand: Optional[str] = Field(None, max_length=255)
    size: Optional[str] = Field(None, max_length=50)
    material: Optional[str] = Field(None, max_length=255)
    image_url: str = Field(..., min_length=1, max_length=500)


class ClothingCreate(ClothingBase):
    """Schema for creating a new clothing item."""

    pass


class ClothingUpdate(BaseModel):
    """Schema for updating a clothing item."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = None
    style: Optional[str] = None
    season: Optional[str] = None
    brand: Optional[str] = Field(None, max_length=255)
    size: Optional[str] = Field(None, max_length=50)
    material: Optional[str] = Field(None, max_length=255)
    image_url: Optional[str] = Field(None, min_length=1, max_length=500)


class ClothingResponse(ClothingBase):
    """Schema for clothing response."""

    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

    @property
    def color_list(self) -> List[str]:
        """Parse color JSON string to list."""
        if self.color:
            try:
                return json.loads(self.color)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    @property
    def style_list(self) -> List[str]:
        """Parse style JSON string to list."""
        if self.style:
            try:
                return json.loads(self.style)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    @property
    def season_list(self) -> List[str]:
        """Parse season JSON string to list."""
        if self.season:
            try:
                return json.loads(self.season)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
