from pydantic import BaseModel
from typing import List, Optional
import datetime
from app.models.models import ProductStatus

class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True

class VariantBase(BaseModel):
    sku: str
    sku_name: str
    price_adjustment: float = 0.0
    stock_quantity: int = 0

class VariantCreate(VariantBase):
    pass

class Variant(VariantBase):
    id: int
    product_id: int
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    base_price: float
    status: ProductStatus = ProductStatus.ACTIVE
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    variants: List[Variant] = []
    class Config:
        from_attributes = True

class PriceBreakdown(BaseModel):
    rule_name: str
    discount_amount: float
    description: str

class PriceCalculationResult(BaseModel):
    base_price: float
    final_price: float
    applied_rules: List[PriceBreakdown]

class CartItemAdd(BaseModel):
    variant_id: int
    quantity: int
    cart_id: str
    user_tier: Optional[str] = None
    promo_code: Optional[str] = None

class CheckoutRequest(BaseModel):
    cart_id: str

class PricingRuleBase(BaseModel):
    name: str
    type: str  # BULK, USER_TIER, SEASONAL
    priority: int = 0
    parameters: dict
    is_active: bool = True

class PricingRuleCreate(PricingRuleBase):
    pass

class PricingRule(PricingRuleBase):
    id: int
    class Config:
        from_attributes = True

class OrderItem(BaseModel):
    variant_id: int
    quantity: int
    unit_price: float
    class Config:
        from_attributes = True

class Order(BaseModel):
    id: int
    cart_id: str
    total_amount: float
    created_at: datetime.datetime
    items: List[OrderItem]
    class Config:
        from_attributes = True

class PromotionBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: datetime.datetime
    end_date: datetime.datetime
    discount_percentage: float
    target_category_id: Optional[int] = None
    is_active: bool = True

class PromotionCreate(PromotionBase):
    pass

class Promotion(PromotionBase):
    id: int
    class Config:
        from_attributes = True
