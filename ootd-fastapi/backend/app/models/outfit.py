"""Outfit and OutfitItem models."""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Outfit(Base):
    """Outfit model for clothing combinations."""

    __tablename__ = "outfits"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Outfit info
    name = Column(String(255), nullable=False)
    style = Column(String(100), nullable=False)  # 风格描述
    occasion = Column(String(100), nullable=True)  # 场合
    season = Column(String(50), nullable=True)  # 季节

    # AI generation
    ai_generated = Column(Boolean, default=False, nullable=False)
    result_url = Column(String(500), nullable=True)  # AI 生成的效果图
    prompt = Column(Text, nullable=True)  # 生成提示词

    # AI advice
    reasoning = Column(Text, nullable=True)  # 搭配理由
    tips = Column(Text, nullable=True)  # 穿搭小贴士 JSON array

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="outfits")
    items = relationship("OutfitItem", back_populates="outfit", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Outfit(id={self.id}, name={self.name}, ai_generated={self.ai_generated})>"


class OutfitItem(Base):
    """Junction table for Outfit and Clothing."""

    __tablename__ = "outfit_items"

    id = Column(String(36), primary_key=True, index=True)
    outfit_id = Column(String(36), ForeignKey("outfits.id", ondelete="CASCADE"), nullable=False)
    clothing_id = Column(String(36), ForeignKey("clothing.id", ondelete="CASCADE"), nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    outfit = relationship("Outfit", back_populates="items")
    clothing = relationship("Clothing", back_populates="outfit_items")

    def __repr__(self):
        return f"<OutfitItem(outfit_id={self.outfit_id}, clothing_id={self.clothing_id})>"
