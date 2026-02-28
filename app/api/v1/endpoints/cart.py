from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.inventory import InventoryService
from app.schemas import schemas

router = APIRouter()

@router.post("/add", response_model=schemas.Variant)
def add_to_cart(item: schemas.CartItemAdd, db: Session = Depends(get_db)):
    try:
        reservation = InventoryService.reserve_inventory(
            db, 
            variant_id=item.variant_id, 
            cart_id=item.cart_id, 
            quantity=item.quantity
        )
        return reservation.variant
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/checkout")
def checkout(request: schemas.CheckoutRequest, db: Session = Depends(get_db)):
    try:
        InventoryService.complete_checkout(db, cart_id=request.cart_id)
        return {"message": "Checkout completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/update", response_model=schemas.Variant)
def update_cart_item(item: schemas.CartItemAdd, db: Session = Depends(get_db)):
    # Simple implementation: release old and create new reservation
    from app.models.models import InventoryReservation, ReservationStatus
    db.query(InventoryReservation).filter(
        InventoryReservation.cart_id == item.cart_id,
        InventoryReservation.variant_id == item.variant_id,
        InventoryReservation.status == ReservationStatus.PENDING
    ).update({"status": ReservationStatus.RELEASED})
    db.commit()
    
    return add_to_cart(item, db)

@router.delete("/remove")
def remove_from_cart(cart_id: str, variant_id: int, db: Session = Depends(get_db)):
    from app.models.models import InventoryReservation, ReservationStatus
    res = db.query(InventoryReservation).filter(
        InventoryReservation.cart_id == cart_id,
        InventoryReservation.variant_id == variant_id,
        InventoryReservation.status == ReservationStatus.PENDING
    ).first()
    if not res:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    res.status = ReservationStatus.RELEASED
    db.commit()
    return {"message": "Item removed from cart"}
