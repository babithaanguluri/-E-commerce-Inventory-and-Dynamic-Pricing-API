from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ProductStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    parent = relationship("Category", remote_side=[id], backref="children")
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    base_price = Column(Float, nullable=False)
    status = Column(Enum(ProductStatus), default=ProductStatus.ACTIVE)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")
    variants = relationship("ProductVariant", back_populates="product")

class ProductVariant(Base):
    __tablename__ = "product_variants"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    sku = Column(String, unique=True, index=True, nullable=False)
    sku_name = Column(String, nullable=False) # e.g. "Red / XL"
    price_adjustment = Column(Float, default=0.0)
    stock_quantity = Column(Integer, default=0)

    product = relationship("Product", back_populates="variants")
    reservations = relationship("InventoryReservation", back_populates="variant")

class ReservationStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    RELEASED = "RELEASED"

class InventoryReservation(Base):
    __tablename__ = "inventory_reservations"
    id = Column(Integer, primary_key=True, index=True)
    variant_id = Column(Integer, ForeignKey("product_variants.id"))
    cart_id = Column(String, index=True) # Could be a session ID or user ID
    quantity = Column(Integer, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.PENDING)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    variant = relationship("ProductVariant", back_populates="reservations")

class PricingRuleType(str, enum.Enum):
    BULK = "BULK"
    USER_TIER = "USER_TIER"
    SEASONAL = "SEASONAL"

class PricingRule(Base):
    __tablename__ = "pricing_rules"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(PricingRuleType), nullable=False)
    priority = Column(Integer, default=0)
    parameters = Column(JSON, nullable=False) # e.g. {"min_quantity": 10, "discount": 0.1}
    is_active = Column(Integer, default=1) # 1 for True, 0 for False (using int for simplicity with some SQL dialects)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(String, index=True, nullable=False)
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    variant_id = Column(Integer, ForeignKey("product_variants.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False) # Snapshot price at time of purchase
    
    order = relationship("Order", back_populates="items")
    variant = relationship("ProductVariant")

class Promotion(Base):
    __tablename__ = "promotions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    discount_percentage = Column(Float, nullable=False) # e.g., 0.20 for 20%
    target_category_id = Column(Integer, ForeignKey("categories.id"), nullable=True) # Null means site-wide
    is_active = Column(Integer, default=1)

    category = relationship("Category")
