from sqlalchemy import (
    Integer,
    Float,
    Column,
    ForeignKey
)
from sqlalchemy.orm import relationship

from src.utils.db import Base


class PurchaseItemModel(Base):
    __tablename__ = "purchase_items"

    id = Column(Integer, primary_key=True, index=True)

    purchase_id = Column(
        Integer,
        ForeignKey("purchases.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    unit_price = Column(
        Float,
        nullable=False
    )

    subtotal = Column(
        Float,
        nullable=False
    )

    purchase = relationship(
        "PurchaseModel",
        back_populates="items"
    )

    product = relationship(
        "ProductModel",
        back_populates="purchase_items"
    )