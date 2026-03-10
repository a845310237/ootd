"""Outfit model for outfit combinations."""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class Outfit(Base):
    """
    Outfit model representing outfit combinations.

    Attributes:
        id: Unique outfit identifier (CUID string)
        user_id: ID of the user who created this outfit
        name: Name/description of the outfit
        style: Style description
        occasion: Occasion for the outfit
        season: Season for the outfit
        ai_generated: Whether this was AI-generated
        result_url: URL to AI-generated outfit image
        prompt: Prompt used for AI generation
        reasoning: Explanation of the outfit choices
        tips: JSON array of styling tips
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "outfits"

    id = Column(String(255), primary_key=True, index=True)
    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    style = Column(String(100), nullable=False, index=True)
    occasion = Column(String(100), nullable=True)
    season = Column(String(50), nullable=True)
    ai_generated = Column(Boolean, default=False)
    result_url = Column(String(500), nullable=True)
    prompt = Column(Text, nullable=True)
    reasoning = Column(Text, nullable=True)
    tips = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="outfits")
    items = relationship("OutfitItem", back_populates="outfit", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Outfit(id={self.id}, name={self.name}, style={self.style})>"
