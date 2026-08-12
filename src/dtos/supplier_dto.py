from datetime import datetime
from pydantic import BaseModel, EmailStr


class SupplierCreate(BaseModel):
    name: str
    company_name: str
    email: EmailStr
    phone: str
    address: str | None = None


class SupplierUpdate(BaseModel):
    name: str | None = None
    company_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None


class SupplierResponse(BaseModel):
    id: int
    name: str
    company_name: str
    email: EmailStr
    phone: str
    address: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }