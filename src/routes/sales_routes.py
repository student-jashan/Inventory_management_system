from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.utils.db import get_db

from src.controllers.sales_controller import create_sale,get_all_sales,get_by_id,update_sale,delete_sale
from typing import List
from src.dtos.sales_dto import SaleCreate, SaleResponse
from src.utils.auth import require_sales_user, require_admin
from src.models.user import UserModel

sales_router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)


@sales_router.post("/",response_model=SaleResponse,status_code=status.HTTP_201_CREATED)
def create_new_sale(sale: SaleCreate,db: Session = Depends(get_db), current_user: UserModel = Depends(require_sales_user)):
    return create_sale(sale,db)

@sales_router.get("/all_sales",response_model=List[SaleResponse],status_code = status.HTTP_200_OK)
def get_sales(db:Session = Depends(get_db),current_user: UserModel = Depends(require_sales_user)):
    return get_all_sales(db)

@sales_router.get("/sales/{sales_id}",response_model = SaleResponse)
def get_sales_by_id (sales_id:int,db:Session = Depends(get_db),current_user: UserModel = Depends(require_sales_user)):
    return get_by_id(sales_id,db)

@sales_router.put("/update/{sales_id}",response_model=SaleResponse)
def update_sale_route(sales_id: int, sales: SaleCreate,db: Session = Depends(get_db),current_user: UserModel = Depends(require_sales_user)):
    return update_sale(sales_id,sales,db)


@sales_router.delete("/delete/{sales_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_sale_endpoint(sales_id: int,db: Session = Depends(get_db), current_user: UserModel = Depends(require_admin)):
    return delete_sale(sales_id,db)