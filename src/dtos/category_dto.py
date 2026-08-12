from datetime import datetime

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None
    
    
class CategoryUpdate(BaseModel):
    name: str
    description: str | None = None
    
    
class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
