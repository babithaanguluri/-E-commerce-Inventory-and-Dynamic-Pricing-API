from sqlalchemy.orm import Session
from app.models.models import Category, Product, ProductVariant
from typing import List, Optional

class ProductService:
    @staticmethod
    def get_product(db: Session, product_id: int):
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def get_products(db: Session, q: str = None, skip: int = 0, limit: int = 100):
        from app.models.models import Product
        query = db.query(Product)
        if q:
            query = query.filter(
                (Product.name.ilike(f"%{q}%")) | 
                (Product.description.ilike(f"%{q}%"))
            )
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_product(db: Session, product_data: dict):
        db_product = Product(**product_data)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

class CategoryService:
    @staticmethod
    def get_categories(db: Session):
        return db.query(Category).all()

    @staticmethod
    def create_category(db: Session, category_data: dict):
        db_category = Category(**category_data)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def get_category_hierarchy(db: Session, category_id: int):
        # Implementation for hierarchical categories can be complex,
        # starting with a simple parent fetch.
        return db.query(Category).filter(Category.id == category_id).first()
