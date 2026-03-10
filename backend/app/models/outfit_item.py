"""OutfitItem model for the junction table between Outfit and Clothing."""
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class OutfitItem(Base):
    """
    OutfitItem model representing the relationship between outfits and clothing items.

    This is a junction table that allows many-to-many relationships
    between outfits and clothing items.

    Attributes:
        id: Unique identifier (CUID string)
        outfit_id: ID of the outfit
        clothing_id: ID of the clothing item
        created_at: Creation timestamp
    """

    __tablename__ = "outfit_items"

    id = Column(String(255), primary_key=True, index=True)
    outfit_id = Column(String(255), ForeignKey("outfits.id", ondelete="CASCADE"), nullable=False, index=True)
    clothing_id = Column(String(255), ForeignKey("clothing.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    outfit = relationship("Outfit", back_populates="items")
    clothing = relationship("Clothing", back_populates="outfit_items")

    def __repr__(self):
        return f"<OutfitItem(outfit_id={self.outfit_id}, clothing_id={self.clothing_id})>"
