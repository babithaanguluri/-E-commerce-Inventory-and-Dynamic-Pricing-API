from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.api import deps
from app.services.products import CategoryService
from app.schemas import schemas
from app.models.models import Category, User

router = APIRouter()

@router.get("/", response_model=List[schemas.Category])
def read_categories(db: Session = Depends(get_db)):
    return CategoryService.get_categories(db)

@router.post("/", response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_admin)
):
    return CategoryService.create_category(db, category.model_dump())

@router.put("/{category_id}", response_model=schemas.Category)
def update_category(
    category_id: int, 
    category: schemas.CategoryCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_admin)
):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    for var, value in category.model_dump().items():
        setattr(db_category, var, value)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_id}")
def delete_category(
    category_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_admin)
):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted"}
