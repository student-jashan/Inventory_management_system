from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.utils.db import get_db
from src.dtos.purchase_dto import PurchaseCreate, PurchaseResponse
from src.controllers.purchase_controller import create_purchase,get_all_purchases,get_purchase_by_id,update_purchase,delete_purchase
from src.models.user import UserModel
from src.utils.auth import require_inventory_manager,require_admin

purchase_routes = APIRouter(
    prefix="/purchase",
    tags=["Purchase"]
)


@purchase_routes.post("/",response_model=PurchaseResponse,status_code=status.HTTP_201_CREATED)
def add_purchase(body: PurchaseCreate,db: Session = Depends(get_db),current_user: UserModel = Depends(require_inventory_manager)):
    return create_purchase(body,db)

@purchase_routes.get("/all_purchase",response_model=list[PurchaseResponse],status_code = status.HTTP_200_OK)
def get_purchase(db:Session = Depends(get_db),current_user: UserModel = Depends(require_inventory_manager)):
    return get_all_purchases(db)


@purchase_routes.get("/purchase/{purchase_id}",response_model=PurchaseResponse)
def get_by_id_endpoint(purchase_id:int,db:Session = Depends(get_db),current_user: UserModel = Depends(require_inventory_manager)):
    return get_purchase_by_id(purchase_id,db)

@purchase_routes.put("/update/{purchase_id}",response_model=PurchaseResponse)
def update_purchase_route(purchase_id: int,body: PurchaseCreate,db: Session = Depends(get_db),current_user: UserModel = Depends(require_inventory_manager)):
    return update_purchase(purchase_id,body,db)

@purchase_routes.delete("/delete/{purchase_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_purchase_endpoint(purchase_id: int,db: Session = Depends(get_db),current_user: UserModel = Depends(require_admin)):
    return delete_purchase(purchase_id,db)