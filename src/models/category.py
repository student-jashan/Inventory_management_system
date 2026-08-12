from sqlalchemy import String, Integer, DateTime, Column
from sqlalchemy.orm import relationship
from datetime import datetime

from src.utils.db import Base

class CategoryModel(Base):
    __tablename__ = "category"
    
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(100), unique = True, nullable = False)
    description = Column(String(255), nullable = True)
    created_at = Column(DateTime, default = datetime.utcnow)
    updated_at = Column(DateTime,default = datetime.utcnow, onupdate=datetime.utcnow)

    products = relationship("ProductModel", back_populates="category")