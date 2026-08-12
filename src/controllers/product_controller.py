from src.dtos.category_dto import CategoryCreate
from sqlalchemy.orm import Session
from src.dtos.product_dto import ProductCreate
from src.models.product import ProductModel
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

def create_product(body: ProductCreate, db: Session):
    data = body.model_dump()

    new_product = ProductModel(
        name=data["name"],
        description=data["description"],
        sku=data["sku"],
        price=data["price"],
        quantity=data["quantity"],
        category_id=data["category_id"]
    )

    db.add(new_product)

    try:
        db.commit()
        db.refresh(new_product)

    except IntegrityError as e:
        db.rollback()

        if "products_sku_key" in str(e.orig):
            raise HTTPException(
                status_code=409,
                detail="Product SKU already exists"
            )

        raise HTTPException(
            status_code=400,
            detail="Product could not be created"
        )

    return new_product

def get_products(db:Session):
    products = db.query(ProductModel).all()
    return products


def get_product_by_id(product_id: int, db: Session):
    product = db.query(ProductModel).get(product_id)
    if not product:
        raise HTTPException(404, detail = "Product not found")
    return product

def update_product(body: ProductCreate, product_id: int, db: Session):
    product = db.get(ProductModel, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    body = body.model_dump()

    for field, value in body.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product



def delete_product(product_id:int,db:Session):
    product = db.get(ProductModel, product_id)    
    if not product:
        raise HTTPException(404, detail = "Product not found")
    
    db.delete(product)
    db.commit()
    
    return None
