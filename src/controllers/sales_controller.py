from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.sales import SaleModel
from src.models.sales_item import SaleItemModel
from src.models.product import ProductModel
from sqlalchemy.orm import joinedload
from src.dtos.sales_dto import SaleCreate



def create_sale(sale: SaleCreate, db: Session):

    data = sale.model_dump()

    total_amount = 0

    new_sale = SaleModel(
        invoice_number=data["invoice_number"],
        customer_name=data["customer_name"],
        sale_date=data["sale_date"],
        status="Completed",
        total_amount=0
    )

    db.add(new_sale)
    db.flush()

    for item in data["items"]:
        
        # quantity should not be negative
        if item["quantity"] <= 0:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Sale quantity must be greater than 0"
    )

        product = db.query(ProductModel).filter(
            ProductModel.id == item["product_id"]
        ).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item['product_id']} not found"
            )

        # Check stock availability
        if product.quantity < item["quantity"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for {product.name}"
            )

        # Reduce stock
        product.quantity -= item["quantity"]

        subtotal = item["quantity"] * item["unit_price"]

        sale_item = SaleItemModel(
            sale_id=new_sale.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            unit_price=item["unit_price"],
            subtotal=subtotal
        )

        db.add(sale_item)

        total_amount += subtotal

    new_sale.total_amount = total_amount

    db.commit()
    db.refresh(new_sale)

    return new_sale

def get_all_sales(db: Session):
    sales = db.query(SaleModel).all()
    return sales

def get_by_id(sales_id: int, db: Session):

    sale = (
        db.query(SaleModel)
        .options(
            joinedload(SaleModel.items)
        )
        .filter(SaleModel.id == sales_id)
        .first()
    )

    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )

    return sale
    
def update_sale(
    sale_id: int,
    sale: SaleCreate,
    db: Session
):
    data = sale.model_dump()

    # Check if sale exists
    existing_sale = db.query(SaleModel).filter(
        SaleModel.id == sale_id
    ).first()

    if not existing_sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )

    # Restore previous stock
    old_items = db.query(SaleItemModel).filter(
        SaleItemModel.sale_id == sale_id
    ).all()

    for item in old_items:

        product = db.query(ProductModel).filter(
            ProductModel.id == item.product_id
        ).first()

        if product:
            product.quantity += item.quantity

    # Delete old sale items
    db.query(SaleItemModel).filter(
        SaleItemModel.sale_id == sale_id
    ).delete()

    # Update sale details
    existing_sale.invoice_number = data["invoice_number"]
    existing_sale.customer_name = data["customer_name"]
    existing_sale.sale_date = data["sale_date"]

    total_amount = 0

    # Add updated sale items
    for item in data["items"]:

        product = db.query(ProductModel).filter(
            ProductModel.id == item["product_id"]
        ).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item['product_id']} not found"
            )

        # Check stock
        if product.quantity < item["quantity"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for {product.name}"
            )

        # Reduce stock
        product.quantity -= item["quantity"]

        subtotal = item["quantity"] * item["unit_price"]

        sale_item = SaleItemModel(
            sale_id=existing_sale.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            unit_price=item["unit_price"],
            subtotal=subtotal
        )

        db.add(sale_item)

        total_amount += subtotal

    existing_sale.total_amount = total_amount

    db.commit()
    db.refresh(existing_sale)

    return existing_sale


def delete_sale(sale_id: int, db: Session):

    # Check if sale exists
    sale = db.query(SaleModel).filter(
        SaleModel.id == sale_id
    ).first()

    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )

    # Get all sale items
    sale_items = db.query(SaleItemModel).filter(
        SaleItemModel.sale_id == sale_id
    ).all()

    # Restore stock
    for item in sale_items:

        product = db.query(ProductModel).filter(
            ProductModel.id == item.product_id
        ).first()

        if product:
            product.quantity += item.quantity

    # Delete sale items
    db.query(SaleItemModel).filter(
        SaleItemModel.sale_id == sale_id
    ).delete()

    # Delete sale
    db.delete(sale)

    db.commit()

    return {
        "message": "Sale deleted successfully"
    }