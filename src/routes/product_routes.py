from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.controllers.category_controller import create_category, get_category
from src.controllers.category_controller import create_category
from src.dtos.product_dto import ProductCreate, ProductResponse
from src.utils.db import get_db
from src.controllers.product_controller import create_product, get_product_by_id, get_products,update_product,delete_product
from src.utils.auth import require_admin, get_current_user, require_authenticated_user, require_inventory_manager
from src.models.user import UserModel
product_routes = APIRouter(prefix = "/product")

@product_routes.post("/create", response_model = ProductResponse, status_code = status.HTTP_201_CREATED)
def create_product_endpoint(body:ProductCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(require_admin)):
    return create_product(body,db)


@product_routes.get("/all_products",response_model=list[ProductResponse],status_code = status.HTTP_200_OK)
def get_all_products(db:Session = Depends(get_db),current_user : UserModel = Depends(get_current_user)):
    return get_products(db)

# 
@product_routes.get("/product/{product_id}", response_model = ProductResponse, status_code = status.HTTP_200_OK)
def get_product_endpoint(product_id: int, db:Session = Depends(get_db), current_user: UserModel = Depends(require_authenticated_user)):
    return get_product_by_id(product_id, db)


@product_routes.put("/update/product/{product_id}",response_model = ProductResponse, status_code = status.HTTP_200_OK)
def update_product_endpoint(body:ProductCreate, product_id:int, db:Session = Depends(get_db),current_user: UserModel = Depends(require_inventory_manager)):
    return update_product(body,product_id,db)

@product_routes.delete("/delete/product/{product_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_product_endpoint(product_id:int,db:Session=Depends(get_db),current_user:UserModel = Depends(require_admin)):
    return delete_product(product_id,db)



