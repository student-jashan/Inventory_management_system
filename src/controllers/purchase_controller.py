from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException, status

from src.models.purchase import PurchaseModel
from src.models.purchase_items import PurchaseItemModel
from src.models.product import ProductModel
from src.models.supplier import SupplierModel

from src.dtos.purchase_dto import PurchaseCreate


def create_purchase(body: PurchaseCreate,db: Session):

    supplier = db.query(SupplierModel).filter(
        SupplierModel.id == body.supplier_id
    ).first()

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )

    new_purchase = PurchaseModel(
        supplier_id=body.supplier_id,
        invoice_number=body.invoice_number,
        purchase_date=body.purchase_date,
        total_amount=0
    )

    db.add(new_purchase)
    db.flush()

    total_amount = 0

    for item in body.items:
        # item quantity should be positive
        
        if item.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Purchase quantity must be greater than 0"
        )

        product = db.query(ProductModel).filter(
            ProductModel.id == item.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item.product_id} not found"
            )

        product.quantity += item.quantity

        subtotal = item.quantity * item.unit_price

        purchase_item = PurchaseItemModel(
            purchase_id=new_purchase.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=subtotal
        )

        db.add(purchase_item)

        total_amount += subtotal

    new_purchase.total_amount = total_amount

    db.commit()
    db.refresh(new_purchase)

    return new_purchase






def get_all_purchases(db: Session):
    purchases = db.query(PurchaseModel).all()
    return purchases

def get_purchase_by_id(purchase_id: int, db: Session):

    purchase = (
        db.query(PurchaseModel)
        .options(
            joinedload(PurchaseModel.supplier),
            joinedload(PurchaseModel.items)
        )
        .filter(PurchaseModel.id == purchase_id)
        .first()
    )

    if not purchase:
        raise HTTPException(
            status_code=404,
            detail="Purchase not found"
        )

    return purchase

def update_purchase(
    purchase_id: int,
    purchase: PurchaseCreate,
    db: Session
):
    data = purchase.model_dump()

    # Check if purchase exists
    existing_purchase = db.query(PurchaseModel).get(purchase_id)

    if not existing_purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase not found"
        )

    # Check if supplier exists
    supplier = db.query(SupplierModel).get(data["supplier_id"])

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )

    # Reverse previous stock
    old_items = db.query(PurchaseItemModel).filter(
        PurchaseItemModel.purchase_id == purchase_id
    ).all()

    for item in old_items:
        product = db.query(ProductModel).get(item.product_id)

        if product:
            product.quantity -= item.quantity

    # Delete previous purchase items
    db.query(PurchaseItemModel).filter(
        PurchaseItemModel.purchase_id == purchase_id
    ).delete()

    # Update purchase details
    existing_purchase.supplier_id = data["supplier_id"]
    existing_purchase.invoice_number = data["invoice_number"]
    existing_purchase.purchase_date = data["purchase_date"]

    total_amount = 0

    # Add new purchase items
    for item in data["items"]:

        product = db.query(ProductModel).get(item["product_id"])

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item['product_id']} not found"
            )

        # Increase stock
        product.quantity += item["quantity"]

        subtotal = item["quantity"] * item["unit_price"]

        purchase_item = PurchaseItemModel(
            purchase_id=existing_purchase.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            unit_price=item["unit_price"],
            subtotal=subtotal
        )

        db.add(purchase_item)

        total_amount += subtotal

    existing_purchase.total_amount = total_amount

    db.commit()
    db.refresh(existing_purchase)

    return existing_purchase


def delete_purchase(purchase_id: int, db: Session):

    purchase = db.query(PurchaseModel).filter(
        PurchaseModel.id == purchase_id
    ).first()

    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase not found"
        )

    purchase_items = db.query(PurchaseItemModel).filter(
        PurchaseItemModel.purchase_id == purchase_id
    ).all()

    # Reverse stock
    for item in purchase_items:

        product = db.query(ProductModel).filter(
            ProductModel.id == item.product_id
        ).first()

        if product:
            product.quantity -= item.quantity

    # Delete purchase items
    db.query(PurchaseItemModel).filter(
        PurchaseItemModel.purchase_id == purchase_id
    ).delete()

    # Delete purchase
    db.delete(purchase)

    db.commit()

    return None