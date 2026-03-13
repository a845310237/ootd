"""User model."""
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class User(Base):
    """User model for authentication and profile."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    password = Column(String(255), nullable=False)

    # Body characteristics
    height = Column(Integer, nullable=True)  # cm
    weight = Column(Integer, nullable=True)  # kg
    body_type = Column(String(50), nullable=True)  # 体型: 苗条/标准/丰满
    skin_tone = Column(String(50), nullable=True)  # 肤色
    avatar = Column(String(500), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    clothes = relationship("Clothing", back_populates="user", cascade="all, delete-orphan")
    outfits = relationship("Outfit", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
