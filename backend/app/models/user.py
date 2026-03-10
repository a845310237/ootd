"""User model for authentication and profile information."""
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class User(Base):
    """
    User model representing application users.

    Attributes:
        id: Unique user identifier (CUID string)
        email: User's email address (unique)
        name: User's display name
        password: Hashed password
        height: User's height in centimeters
        weight: User's weight in kilograms
        body_type: User's body type classification
        skin_tone: User's skin tone
        avatar: URL to user's avatar image
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "users"

    id = Column(String(255), primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)
    password = Column(String(255), nullable=False)
    height = Column(Integer, nullable=True)  # cm
    weight = Column(Integer, nullable=True)  # kg
    body_type = Column(String(50), nullable=True)
    skin_tone = Column(String(50), nullable=True)
    avatar = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    clothes = relationship("Clothing", back_populates="user", cascade="all, delete-orphan")
    outfits = relationship("Outfit", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"
