from src.dtos.category_dto import CategoryCreate
from sqlalchemy.orm import Session
from src.models.category import CategoryModel
from fastapi import HTTPException, status

def create_category(body:CategoryCreate,db: Session):
    data = body.model_dump()
    
    new_category = CategoryModel(
        name = data["name"],
        description = data["description"]
    )
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return new_category

def get_category(db:Session):
    category = db.query(CategoryModel).all()
    return category


def get_category_by_id(category_id:int,db:Session):
    one_category = db.query(CategoryModel).get(category_id)
    if not one_category:
        raise HTTPException(404, detail = "Category not found")
    
    return one_category

def update_category(body:CategoryCreate, category_id:int, db:Session):
    category = db.query(CategoryModel).get(category_id)
    
    if not category:
        raise HTTPException(404, detail = "Category not found")
    
    body = body.model_dump()
    
    for field, value in body.items():
        setattr(category, field, value)
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    return category

def delete_category(category_id:int,db:Session):
    category = db.query(CategoryModel).get(category_id)
    
    if not category:
        raise HTTPException(404, detail = "Category not found")
    
    db.delete(category)
    db.commit()
    
    return None