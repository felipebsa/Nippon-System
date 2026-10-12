from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User
from schemas.user import SchemaRegister, SchemaUserResponse
from database import get_db
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone

load_dotenv()
router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRE_DAYS = 7
PASSWORD_MIN_LENGTH = 8

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

@router.get("/")
def auth_home():
    return {"message": "auth_home successful"}

@router.post("/auth/register")
def create_user(user: SchemaRegister, db: Session = Depends(get_db), _=Depends(get_current_user)):
    if len(user.password) < PASSWORD_MIN_LENGTH:
        raise HTTPException(status_code=400, detail=f"A senha deve ter no mínimo {PASSWORD_MIN_LENGTH} caracteres.")
    query = select(User).where(User.username==user.username)
    db_user = db.execute(query).scalars().first()
    if db_user:
        raise HTTPException(status_code=409, detail="username exists")
    hash_created = pwd_context.hash(user.password)
    post_user = User(
        username = user.username,
        pass_hash = hash_created
    )
    db.add(post_user)
    db.commit()
    return {"message": "successful create_user"}

@router.post("/auth/login")
def acess_user(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    query = select(User).where(User.username==user.username)
    db_user = db.execute(query).scalars().first()
    if db_user is None or not pwd_context.verify(user.password, db_user.pass_hash):
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos.")
    payload = {
        "user_id": db_user.user_id,
        "username": db_user.username,
        "exp": datetime.now(timezone.utc) + timedelta(days=TOKEN_EXPIRE_DAYS)
    }
    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}