from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import PricingRule

router = APIRouter()

@router.get("/", response_model=List[schemas.PricingRule])
def read_rules(db: Session = Depends(get_db)):
    return db.query(PricingRule).all()

@router.post("/", response_model=schemas.PricingRule)
def create_rule(rule: schemas.PricingRuleCreate, db: Session = Depends(get_db)):
    db_rule = PricingRule(**rule.model_dump())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

@router.delete("/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    db_rule = db.query(PricingRule).filter(PricingRule.id == rule_id).first()
    if not db_rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    db.delete(db_rule)
    db.commit()
    return {"message": "Pricing rule deleted"}
