from datetime import datetime
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=2)
    description: str | None = None
    sku: str = Field(min_length=2)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)
    category_id: int = Field(gt=0)
    
class ProductUpdate(BaseModel):
    name: str
    description: str | None = None
    sku: str
    price: float
    quantity: int
    category_id: int


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    sku: str
    price: float
    quantity: int
    category_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }