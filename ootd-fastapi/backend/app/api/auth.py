"""Authentication API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from uuid import uuid4

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user_in: User creation data
        db: Database session

    Returns:
        Created user

    Raises:
        HTTPException: If email already exists or password hashing fails
    """
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    try:
        # Create new user with password hash
        user = User(
            id=str(uuid4()),
            email=user_in.email,
            name=user_in.name,
            password=get_password_hash(user_in.password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login with email and password.

    Args:
        form_data: OAuth2 form data with username (email) and password
        db: Database session

    Returns:
        Access token and user info

    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email (username in OAuth2 form)
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/logout")
async def logout():
    """
    Logout user.

    Note: With JWT tokens, logout is handled client-side by deleting the token.
    This endpoint exists for future token blacklisting implementation.
    """
    return {"message": "Successfully logged out"}
