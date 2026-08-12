from sqlalchemy import String, Float, Integer, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from src.utils.db import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    sku = Column(String(50), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)

    # NEW: Foreign Key
    category_id = Column(
        Integer,
        ForeignKey("category.id"),   # Change to "categories.id" if your Category table is named "categories"
        nullable=False
    )

    # NEW: Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # NEW: Relationship
    category = relationship("CategoryModel", back_populates="products")
    purchase_items = relationship(
    "PurchaseItemModel",
    back_populates="product"
)
    sale_items = relationship(
    "SaleItemModel",
    back_populates="product"
)
