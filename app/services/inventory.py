from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import ProductVariant, InventoryReservation, ReservationStatus
import datetime

class InventoryService:
    @staticmethod
    def get_available_quantity(db: Session, variant_id: int) -> int:
        variant = db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()
        if not variant:
            return 0
        
        reserved_qty = db.query(func.sum(InventoryReservation.quantity))\
            .filter(
                InventoryReservation.variant_id == variant_id,
                InventoryReservation.status == ReservationStatus.PENDING,
                InventoryReservation.expires_at > datetime.datetime.utcnow()
            ).scalar() or 0
        
        return variant.stock_quantity - reserved_qty

    @staticmethod
    def reserve_inventory(db: Session, variant_id: int, cart_id: str, quantity: int, duration_minutes: int = 15):
        variant = db.query(ProductVariant).filter(ProductVariant.id == variant_id).with_for_update().first()
        
        if not variant:
            raise Exception("Variant not found")
            
        available_qty = InventoryService.get_available_quantity(db, variant_id)
        
        if available_qty < quantity:
            raise Exception("Not enough available inventory")
            
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=duration_minutes)
        
        reservation = InventoryReservation(
            variant_id=variant_id,
            cart_id=cart_id,
            quantity=quantity,
            expires_at=expires_at,
            status=ReservationStatus.PENDING
        )
        
        db.add(reservation)
        db.commit()
        db.refresh(reservation)
        return reservation

    @staticmethod
    def complete_checkout(db: Session, cart_id: str):
        from app.models.models import Order, OrderItem, PricingRule
        from app.services.pricing import PricingEngine
        
        reservations = db.query(InventoryReservation).filter(
            InventoryReservation.cart_id == cart_id,
            InventoryReservation.status == ReservationStatus.PENDING,
            InventoryReservation.expires_at > datetime.datetime.utcnow()
        ).all()
        
        if not reservations:
            raise Exception("No active reservations found for this cart")
            
        total_amount = 0.0
        order = Order(cart_id=cart_id, total_amount=0.0)
        db.add(order)
        db.flush() 
        
        engine = PricingEngine()
        rules = db.query(PricingRule).filter(PricingRule.is_active == 1).order_by(PricingRule.priority.desc()).all()

        for res in reservations:
            variant = db.query(ProductVariant).filter(ProductVariant.id == res.variant_id).with_for_update().first()
            if not variant:
                continue
            
            # Calculate final price using dynamic pricing engine
            product = variant.product
            context = {"quantity": res.quantity} 
            price_result = engine.calculate_price(
                product.base_price + variant.price_adjustment, 
                context, 
                rules, 
                product_category_id=product.category_id, 
                db=db
            )
            unit_price = price_result.final_price
            
            order_item = OrderItem(
                order_id=order.id,
                variant_id=res.variant_id,
                quantity=res.quantity,
                unit_price=unit_price
            )
            db.add(order_item)
            
            total_amount += unit_price * res.quantity
            
            variant.stock_quantity -= res.quantity
            res.status = ReservationStatus.COMPLETED
            
        order.total_amount = total_amount
        db.commit()
        return order

    @staticmethod
    def cleanup_expired_reservations(db: Session):
        expired = db.query(InventoryReservation).filter(
            InventoryReservation.status == ReservationStatus.PENDING,
            InventoryReservation.expires_at <= datetime.datetime.utcnow()
        ).all()
        
        for res in expired:
            res.status = ReservationStatus.RELEASED
            
        db.commit()
        return len(expired)
