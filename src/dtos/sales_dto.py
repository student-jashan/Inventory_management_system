from datetime import date
from typing import List

from pydantic import BaseModel, Field, ConfigDict


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)

class SaleCreate(BaseModel):
    invoice_number: str
    customer_name: str
    sale_date: date
    items: List[SaleItemCreate]
    
class SaleItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float

    model_config = ConfigDict(from_attributes=True)
    
class SaleResponse(BaseModel):
    id: int
    invoice_number: str
    customer_name: str
    sale_date: date
    status: str
    total_amount: float
    items: List[SaleItemResponse]

    model_config = ConfigDict(from_attributes=True)
