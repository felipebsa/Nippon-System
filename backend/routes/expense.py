from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas.expense import SchemaExpenseCreate, SchemaExpenseResponse, SchemaExpenseUpdate
from models.expense import Expense
from database import get_db 
from routes.auth import get_current_user

router = APIRouter()

@router.post("/expense/register")
def create_expense(expense: SchemaExpenseCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db_expense = Expense(
        name = expense.name,
        value = expense.value,
        date = expense.date,
        origin = "manual"
    )
    db.add(db_expense)
    db.commit()
    return {"message": "successful create_expense"}

@router.get("/expense/get/all")
def get_all_expense(db: Session = Depends(get_db), _=Depends(get_current_user)):
    query = select(Expense)
    db_expense = db.execute(query).scalars().all()
    if not db_expense:
        raise HTTPException(status_code=404, detail="despesa não encontrada")
    return db_expense

@router.get("/expense/get/id/{id}")
def get_by_id_expense(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    query = select(Expense).where(Expense.expense_id==id)
    db_expense = db.execute(query).scalars().first()
    if db_expense is None:
        raise HTTPException(status_code=404, detail="despesa não encontrada")
    return db_expense

@router.put("/expense/update/{id}")
def update_expense(id: int, expense: SchemaExpenseUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    query = select(Expense).where(Expense.expense_id==id)
    db_expense = db.execute(query).scalars().first()
    if db_expense is None:
        raise HTTPException(status_code=404, detail="despesa não encontrada")
    db_expense.name = expense.name
    db_expense.value = expense.value
    db_expense.date = expense.date
    db.commit()
    return {"message": "succesfull update_expense"}

@router.delete("/expense/delete/{id}")
def delete_expense(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    query = select(Expense).where(Expense.expense_id==id)
    db_expense = db.execute(query).scalars().first()
    if db_expense is None:
        raise HTTPException(status_code=404, detail="despesa não encontrada")
    db.delete(db_expense)
    db.commit()
    return {"message": "succesfull delete_expense"}
