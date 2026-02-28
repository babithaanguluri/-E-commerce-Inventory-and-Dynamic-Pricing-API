from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import Promotion

router = APIRouter()

@router.get("/", response_model=List[schemas.Promotion])
def read_promotions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Promotion).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.Promotion)
def create_promotion(promotion: schemas.PromotionCreate, db: Session = Depends(get_db)):
    db_promotion = Promotion(**promotion.model_dump())
    db.add(db_promotion)
    db.commit()
    db.refresh(db_promotion)
    return db_promotion

@router.delete("/{promotion_id}")
def delete_promotion(promotion_id: int, db: Session = Depends(get_db)):
    db_promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    if not db_promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    db.delete(db_promotion)
    db.commit()
    return {"message": "Promotion deleted"}
