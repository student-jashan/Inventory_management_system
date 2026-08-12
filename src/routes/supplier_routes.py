from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.controllers.supplier_controller import create_supplier, delete_supplier, get_supplier_by_id,get_suppliers,update_supplier
from src.dtos.supplier_dto import SupplierCreate, SupplierResponse
from src.routes import product_routes
from src.utils.db import get_db
from src.utils.auth import require_inventory_manager,require_admin
from src.models.user import UserModel

supplier_routes = APIRouter(prefix = "/supplier")

@supplier_routes.post("/create", response_model = SupplierResponse, status_code = status.HTTP_201_CREATED)
def create_supplier_endpoint(body:SupplierCreate, db: Session = Depends(get_db),current_user: UserModel = Depends(require_inventory_manager)):
    return create_supplier(db, supplier=body)


@supplier_routes.get("/all_suppliers",response_model=list[SupplierResponse],status_code = status.HTTP_200_OK)
def get_all_suppliers(db:Session = Depends(get_db),current_user: UserModel = Depends(require_inventory_manager)):
    return get_suppliers(db)


@supplier_routes.get("/supplier/{supplier_id}",response_model = SupplierResponse, status_code = status.HTTP_200_OK)
def get_supplier_endpoint(supplier_id:int,db:Session = Depends(get_db),current_user: UserModel = Depends(require_inventory_manager)):
    return get_supplier_by_id(supplier_id, db)

@supplier_routes.put("/update/supplier/{supplier_id}",response_model = SupplierResponse, status_code = status.HTTP_200_OK)
def update_supplier_endpoint(body:SupplierCreate, supplier_id:int, db:Session = Depends(get_db),current_user: UserModel = Depends(require_inventory_manager)):
    return update_supplier(body, supplier_id, db)

@supplier_routes.delete("/delete/supplier/{supplier_id}", status_code = status.HTTP_200_OK)
def delete_supplier_endpoint(supplier_id:int,db:Session = Depends(get_db),current_user: UserModel = Depends(require_admin)):
    return delete_supplier(supplier_id, db)