from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User
from schemas.user import SchemaLogin, SchemaRegister, SchemaUserResponse
from database import get_db
from passlib.context import CryptContext

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
    pwd_context = CryptContext(schemes=['bcrypt'])
    hash_created = pwd_context.hash(user.password)
    post_user = User(
        email = user.email,
        pass_hash = hash_created,
        role = user.role
    )
    db.add(post_user)
    db.commit()
    return {"message": "successful create_user"}
