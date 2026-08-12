from datetime import date
from typing import List

from pydantic import BaseModel, Field, ConfigDict

class PurchaseItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    
    
class PurchaseCreate(BaseModel):
    supplier_id: int
    invoice_number: str
    purchase_date: date
    items: List[PurchaseItemCreate]
    
    
class PurchaseItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float

    model_config = ConfigDict(from_attributes=True)
    
    
class PurchaseResponse(BaseModel):
    id: int
    supplier_id: int
    invoice_number: str
    purchase_date: date
    status: str
    total_amount: float
    items: List[PurchaseItemResponse]

    model_config = ConfigDict(from_attributes=True)