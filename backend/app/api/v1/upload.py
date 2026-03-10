"""File upload API routes for image uploads."""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from app.core.deps import get_current_user
from app.models.user import User
from app.core.config import settings
import os
import uuid
from pathlib import Path
from typing import Optional

router = APIRouter(prefix="/upload", tags=["上传"])

# Ensure upload directory exists
UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload an image file.

    Args:
        file: Image file to upload
        current_user: Current authenticated user

    Returns:
        dict: URL of the uploaded file

    Raises:
        HTTPException: If file validation fails
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只支持图片文件"
        )

    # Check file size
    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件大小不能超过 {settings.MAX_UPLOAD_SIZE // (1024 * 1024)}MB"
        )

    # Generate unique filename
    file_ext = file.filename.split(".")[-1] if file.filename else "jpg"
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = UPLOAD_DIR / unique_filename

    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(content)

    # Return URL
    file_url = f"/static/uploads/{unique_filename}"
    return {"url": file_url}

