"""Clothing model."""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Clothing(Base):
    """Clothing model for individual items."""

    __tablename__ = "clothing"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Basic info
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)  # 上衣/裤子/鞋子/配饰等
    color = Column(Text, nullable=True)  # JSON array: ["红色", "蓝色"]
    style = Column(Text, nullable=True)  # JSON array: ["休闲", "运动"]
    season = Column(Text, nullable=True)  # JSON array: ["春", "夏"]

    # Details
    brand = Column(String(255), nullable=True)
    size = Column(String(50), nullable=True)
    material = Column(String(255), nullable=True)
    image_url = Column(String(500), nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="clothes")
    outfit_items = relationship("OutfitItem", back_populates="clothing", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Clothing(id={self.id}, name={self.name}, category={self.category})>"
