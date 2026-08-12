from sqlalchemy import (
    String,
    Float,
    Integer,
    Date,
    DateTime,
    Column
)
from sqlalchemy.orm import relationship
from datetime import datetime

from src.utils.db import Base


class SaleModel(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)

    invoice_number = Column(
        String(100),
        unique=True,
        nullable=False
    )

    customer_name = Column(
        String(100),
        nullable=False
    )

    sale_date = Column(
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

    items = relationship(
        "SaleItemModel",
        back_populates="sale",
        cascade="all, delete-orphan"
    )