"""Pydantic schemas for request/response validation."""
from app.schemas.token import Token, TokenPayload
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserProfileResponse
from app.schemas.clothing import ClothingCreate, ClothingUpdate, ClothingResponse
from app.schemas.outfit import (
    OutfitCreate,
    OutfitUpdate,
    OutfitResponse,
    OutfitDetailResponse,
    OutfitGenerateRequest,
    OutfitItemResponse,
)

__all__ = [
    "Token",
    "TokenPayload",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserProfileResponse",
    "ClothingCreate",
    "ClothingUpdate",
    "ClothingResponse",
    "OutfitCreate",
    "OutfitUpdate",
    "OutfitResponse",
    "OutfitDetailResponse",
    "OutfitGenerateRequest",
    "OutfitItemResponse",
]
