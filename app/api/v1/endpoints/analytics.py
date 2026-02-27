from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from sqlalchemy import func
from app.models.models import ProductVariant, OrderItem

router = APIRouter()

@router.get("/low-stock", response_model=List[schemas.Variant])
def get_low_stock_items(threshold: int = Query(5, ge=0), db: Session = Depends(get_db)):
    """
    Returns all product variants where stock_quantity is below the threshold.
    """
    low_stock_items = db.query(ProductVariant).filter(ProductVariant.stock_quantity < threshold).all()
    return low_stock_items

@router.get("/top-selling")
def get_top_selling_products(limit: int = Query(10, ge=1), db: Session = Depends(get_db)):
    """
    Returns the top selling product variants by quantity sold.
    """
    top_selling = (
        db.query(
            ProductVariant.sku,
            ProductVariant.sku_name,
            func.sum(OrderItem.quantity).label("total_sold")
        )
        .join(OrderItem, ProductVariant.id == OrderItem.variant_id)
        .group_by(ProductVariant.id)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(limit)
        .all()
    )
    return [
        {"sku": item.sku, "name": item.sku_name, "total_sold": item.total_sold}
        for item in top_selling
    ]
