from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.dtos.category_dto import CategoryCreate,CategoryResponse
from src.utils.db import get_db
from src.controllers.category_controller import create_category,get_category, get_category_by_id, update_category, delete_category as delete_category_controller
from src.models.user import UserModel
from src.utils.auth import require_admin, get_current_user, require_authenticated_user, require_inventory_manager

category_routes = APIRouter(prefix = "/category")

@category_routes.post("/create", response_model = CategoryResponse, status_code = status.HTTP_201_CREATED)
def create_category_endpoint(body:CategoryCreate, db: Session = Depends(get_db),current_user: UserModel = Depends(require_admin)):
    return create_category(body,db)


@category_routes.get("/all_categories",response_model=list[CategoryResponse],status_code = status.HTTP_200_OK)
def get_all_categories(db:Session = Depends(get_db),current_user: UserModel = Depends(require_authenticated_user)):
    return get_category(db)

@category_routes.get("/category/{category_id}",response_model = CategoryResponse,status_code = status.HTTP_200_OK)
def get_category_by_id_endpoint(category_id:int, db:Session = Depends(get_db),current_user: UserModel = Depends(require_authenticated_user)):
    return get_category_by_id(category_id,db)


@category_routes.put("/update_category/{category_id}",response_model = CategoryResponse,status_code = status.HTTP_200_OK)
def update_category_endpoint(body:CategoryCreate, category_id:int, db:Session = Depends(get_db),current_user: UserModel = Depends(require_inventory_manager)):
    return update_category(body, category_id, db)


@category_routes.delete("/delete_category/{category_id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_category(category_id:int,db:Session=Depends(get_db),current_user: UserModel = Depends(require_admin)):
    return delete_category_controller(category_id,db)