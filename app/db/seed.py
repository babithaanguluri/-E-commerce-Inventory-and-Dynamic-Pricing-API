from app.db.database import init_db, SessionLocal
from app.models.models import Category, Product, ProductVariant, PricingRule, PricingRuleType
import datetime

def seed_db():
    init_db()
    db = SessionLocal()
    
    # Check if data already exists
    if db.query(Category).first():
        db.close()
        return

    # Categories
    electronics = Category(name="Electronics")
    db.add(electronics)
    db.flush()
    
    laptops = Category(name="Laptops", parent_id=electronics.id)
    db.add(laptops)
    db.flush()
    
    # Product
    macbook = Product(
        name="MacBook Pro",
        description="High-end laptop",
        base_price=2000.0,
        category_id=laptops.id
    )
    db.add(macbook)
    db.flush()
    
    # Variant
    m3_pro = ProductVariant(
        product_id=macbook.id,
        sku="MBP-M3-PRO",
        sku_name="M3 Pro / 16GB / 512GB",
        price_adjustment=500.0,
        stock_quantity=10
    )
    db.add(m3_pro)
    
    # Pricing Rules
    bulk_rule = PricingRule(
        name="Bulk Laptop Discount",
        type=PricingRuleType.BULK,
        priority=1,
        parameters={"min_quantity": 5, "discount_percentage": 0.1}
    )
    db.add(bulk_rule)
    
    seasonal_rule = PricingRule(
        name="Winter Sale",
        type=PricingRuleType.SEASONAL,
        priority=2,
        parameters={"discount_percentage": 0.05}
    )
    db.add(seasonal_rule)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_db()
