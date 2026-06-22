from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from models import User
from schemas import UserOut

router = APIRouter()


@router.get("/me", response_model=UserOut)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.get("/search", response_model=list[UserOut])
def search_users(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    users = db.query(User).filter(
        User.username.contains(query)
    ).limit(10).all()
    return users


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user