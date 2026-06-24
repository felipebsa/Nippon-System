from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User
from schemas.user import SchemaLogin, SchemaRegister, SchemaUserResponse
from database import get_db

router = APIRouter()

@router.get("/")
def auth_home():
    return {"message": "auth_home successful"}

@router.post("auth/register")
def create_user(user: SchemaRegister, db: Session = Depends(get_db)):
    query = select(User).where(User.email==user.email)
    db_user = db.execute(query).scalars().first()
    if db_user:
        raise HTTPException(status_code=409, detail="email exists")
    return {"message": db_user}
