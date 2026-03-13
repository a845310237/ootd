"""Image upload API routes."""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.api.deps import get_current_user
from app.core.config import settings
from app.services.oss_service import oss_service

router = APIRouter(prefix="/upload", tags=["Upload"])


# Allowed image types
ALLOWED_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp", "image/gif"}


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload an image file to Aliyun OSS.

    Args:
        file: Image file to upload
        current_user: Current authenticated user
        db: Database session

    Returns:
        URL of uploaded image

    Raises:
        HTTPException: If file type or size is invalid
    """
    # Check if OSS service is available
    if oss_service is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OSS service is not configured. Please check your OSS credentials in .env file."
        )

    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_TYPES)}"
        )

    # Read file to check size and get content
    contents = await file.read()
    file_size = len(contents)

    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )

    try:
        # Upload to OSS
        url, size = await oss_service.upload_file(
            file_content=contents,
            filename=file.filename or "image.jpg",
            content_type=file.content_type,
            prefix="images"
        )

        return {
            "url": url,
            "size": size,
            "type": file.content_type
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image: {str(e)}"
        )


@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload user avatar to Aliyun OSS.

    Args:
        file: Image file to upload
        current_user: Current authenticated user
        db: Database session

    Returns:
        URL of uploaded avatar

    Raises:
        HTTPException: If file type or size is invalid
    """
    # Check if OSS service is available
    if oss_service is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OSS service is not configured. Please check your OSS credentials in .env file."
        )

    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_TYPES)}"
        )

    # Read file to check size and get content
    contents = await file.read()
    file_size = len(contents)

    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )

    try:
        # Upload to OSS
        url, size = await oss_service.upload_file(
            file_content=contents,
            filename=file.filename or "avatar.jpg",
            content_type=file.content_type,
            prefix="avatars"
        )

        # Update user avatar
        current_user.avatar = url
        db.commit()

        return {
            "url": url,
            "size": size,
            "type": file.content_type
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload avatar: {str(e)}"
        )
