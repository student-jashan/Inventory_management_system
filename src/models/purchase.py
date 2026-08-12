from sqlalchemy import (
    String,
    Float,
    Integer,
    Date,
    DateTime,
    Column,
    ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime

from src.utils.db import Base


class PurchaseModel(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)

    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id"),
        nullable=False
    )

    invoice_number = Column(
        String(100),
        unique=True,
        nullable=False
    )

    purchase_date = Column(
        Date,
        nullable=False
    )

    status = Column(
        String(50),
        default="Completed"
    )

    total_amount = Column(
        Float,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    supplier = relationship(
        "SupplierModel",
        back_populates="purchases"
    )

    items = relationship(
        "PurchaseItemModel",
        back_populates="purchase",
        cascade="all, delete-orphan"
    )