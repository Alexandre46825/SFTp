from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserOut, LoginRequest, Token
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM  = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router      = APIRouter()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", response_model=UserOut)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.mail == user_data.mail).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username déjà utilisé")

    new_user = User(
        name=user_data.name,
        surname=user_data.surname,
        username=user_data.username,
        mail=user_data.mail,
        password=hash_password(user_data.password),
        location=user_data.location
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.mail == credentials.mail).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    token = create_token({"sub": str(user.id_user), "username": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register-admin", response_model=UserOut)
def register_admin(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(__import__('dependencies').get_admin_user)
):
    if db.query(User).filter(User.mail == user_data.mail).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username déjà utilisé")

    new_user = User(
        name=user_data.name,
        surname=user_data.surname,
        username=user_data.username,
        mail=user_data.mail,
        password=hash_password(user_data.password),
        location=user_data.location,
        is_admin=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user