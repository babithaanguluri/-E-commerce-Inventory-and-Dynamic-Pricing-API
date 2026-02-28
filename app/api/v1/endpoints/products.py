from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.services.products import ProductService
from app.services.pricing import PricingEngine
from app.models.models import PricingRule
from app.schemas import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Product])
def read_products(q: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = ProductService.get_products(db, q=q, skip=skip, limit=limit)
    return products

@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return ProductService.create_product(db, product.model_dump())

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    from app.models.models import Product
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for var, value in product.model_dump().items():
        setattr(db_product, var, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    from app.models.models import Product
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted"}

# Variant Endpoints
@router.post("/{product_id}/variants", response_model=schemas.Variant)
def create_variant(product_id: int, variant: schemas.VariantCreate, db: Session = Depends(get_db)):
    from app.models.models import ProductVariant
    db_variant = ProductVariant(**variant.model_dump(), product_id=product_id)
    db.add(db_variant)
    db.commit()
    db.refresh(db_variant)
    return db_variant

@router.put("/variants/{variant_id}", response_model=schemas.Variant)
def update_variant(variant_id: int, variant: schemas.VariantCreate, db: Session = Depends(get_db)):
    from app.models.models import ProductVariant
    db_variant = db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()
    if not db_variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    for var, value in variant.model_dump().items():
        setattr(db_variant, var, value)
    db.commit()
    db.refresh(db_variant)
    return db_variant

@router.delete("/variants/{variant_id}")
def delete_variant(variant_id: int, db: Session = Depends(get_db)):
    from app.models.models import ProductVariant
    db_variant = db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()
    if not db_variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    db.delete(db_variant)
    db.commit()
    return {"message": "Variant deleted"}

@router.get("/{product_id}/price", response_model=schemas.PriceCalculationResult)
def calculate_product_price(
    product_id: int,
    quantity: int = Query(1, ge=1),
    user_tier: Optional[str] = None,
    promo_code: Optional[str] = None,
    db: Session = Depends(get_db)
):
    product = ProductService.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Fetch active rules for this calculation
    # For now, fetching all active rules and the engine will decide which to apply
    rules = db.query(PricingRule).order_by(PricingRule.priority.desc()).all()
    
    context = {
        "quantity": quantity,
        "user_tier": user_tier,
        "promo_code": promo_code
    }
    
    engine = PricingEngine()
    result = engine.calculate_price(product.base_price, context, rules, product_category_id=product.category_id, db=db)
    return result
