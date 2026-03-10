"""API v1 router initialization."""
from fastapi import APIRouter
from app.api.v1 import auth, users, wardrobe, outfits, upload

api_router = APIRouter()

# Register all API routers
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(wardrobe.router)
api_router.include_router(outfits.router)
api_router.include_router(upload.router)
