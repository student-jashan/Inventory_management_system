from src.dtos.supplier_dto import SupplierCreate
from sqlalchemy.orm import Session
from src.models.supplier import SupplierModel
from fastapi import HTTPException, status

def create_supplier(db: Session, supplier: SupplierCreate):

    existing_supplier = (
        db.query(SupplierModel)
        .filter(SupplierModel.email == supplier.email)
        .first()
    )

    if existing_supplier:
        raise HTTPException(
            status_code=400,
            detail="Supplier already exists."
        )

    new_supplier = SupplierModel(
        name=supplier.name,
        email=supplier.email,
        phone=supplier.phone,
        company_name=supplier.company_name,
        address=supplier.address
    )

    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)

    return new_supplier



def get_suppliers(db:Session):
    suppliers = db.query(SupplierModel).all()
    return suppliers

def get_supplier_by_id(supplier_id: int, db: Session):
    supplier = db.query(SupplierModel).get(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


def update_supplier(body: SupplierCreate, supplier_id: int, db: Session):
    supplier = db.query(SupplierModel).get(supplier_id)

    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    body = body.model_dump()

    for field, value in body.items():
        setattr(supplier, field, value)

    db.add(supplier)
    db.commit()
    db.refresh(supplier)

    return supplier


def delete_supplier(supplier_id: int, db: Session):
    supplier = db.query(SupplierModel).get(supplier_id)

    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    db.delete(supplier)
    db.commit()

    return None