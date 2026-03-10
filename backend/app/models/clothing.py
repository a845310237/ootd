"""Clothing model for individual clothing items in a user's wardrobe."""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class Clothing(Base):
    """
    Clothing model representing individual clothing items.

    Attributes:
        id: Unique clothing identifier (CUID string)
        user_id: ID of the user who owns this clothing
        name: Name/description of the clothing item
        category: Category (top, bottom, shoes, accessory, etc.)
        color: JSON array of colors
        style: JSON array of styles
        season: JSON array of seasons
        brand: Brand name
        size: Size information
        material: Material information
        image_url: URL to the clothing image
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "clothing"

    id = Column(String(255), primary_key=True, index=True)
    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    color = Column(Text, nullable=True)  # JSON string: ["红色", "蓝色"]
    style = Column(Text, nullable=True)  # JSON string: ["休闲", "运动"]
    season = Column(Text, nullable=True)  # JSON string: ["春", "夏"]
    brand = Column(String(255), nullable=True)
    size = Column(String(50), nullable=True)
    material = Column(String(255), nullable=True)
    image_url = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="clothes")
    outfit_items = relationship("OutfitItem", back_populates="clothing", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Clothing(id={self.id}, name={self.name}, category={self.category})>"
