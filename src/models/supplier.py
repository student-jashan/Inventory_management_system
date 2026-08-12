from sqlalchemy import String, Float, Integer, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from src.utils.db import Base

class SupplierModel(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer,primary_key=True,index = True)
    name = Column(String(100), nullable=False)
    company_name = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(255))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    purchases = relationship(
    "PurchaseModel",
    back_populates="supplier"
)