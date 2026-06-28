from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User
from schemas.user import SchemaLogin, SchemaRegister, SchemaUserResponse
from database import get_db
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer

load_dotenv()
router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=['bcrypt'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid token")
    user_id = payload.get("user_id")
    query = select(User).where(User.user_id==user_id)
    db_user = db.execute(query).scalars().first()
    if not db_user:
        raise HTTPException(status_code=401, detail="id not found")
    return db_user

@router.get("/auth/debug")
def get_debug(c_user = Depends(get_current_user)):
    return {"email": c_user.email, "role": c_user.role}

@router.get("/")
def auth_home():
    return {"message": "auth_home successful"}

@router.post("/auth/register")
def create_user(user: SchemaRegister, db: Session = Depends(get_db)):
    query = select(User).where(User.email==user.email)
    db_user = db.execute(query).scalars().first()
    if db_user:
        raise HTTPException(status_code=409, detail="email exists")
    hash_created = pwd_context.hash(user.password)
    post_user = User(
        email = user.email,
        pass_hash = hash_created,
        role = user.role
    )
    db.add(post_user)
    db.commit()
    return {"message": "successful create_user"}

@router.post("/auth/login")
def acess_user(user: SchemaLogin, db: Session = Depends(get_db)):
    query = select(User).where(User.email==user.email)
    db_user = db.execute(query).scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="email not exists")
    is_valid = pwd_context.verify(user.password, db_user.pass_hash)
    if not is_valid:
        raise HTTPException(status=401, detail="password incorrect")
    payload = {
        "user_id": db_user.user_id,
        "email": db_user.email,
        "role": db_user.role
    }
    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}