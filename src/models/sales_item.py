from sqlalchemy import (
    Integer,
    Float,
    Column,
    ForeignKey
)
from sqlalchemy.orm import relationship

from src.utils.db import Base


class SaleItemModel(Base):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, index=True)

    sale_id = Column(
        Integer,
        ForeignKey("sales.id"),
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

    sale = relationship(
        "SaleModel",
        back_populates="items"
    )

    product = relationship(
        "ProductModel",
        back_populates="sale_items"
    )