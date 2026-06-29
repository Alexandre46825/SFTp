from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from models import User
from schemas import UserOut, PasswordUpdate, ProfileUpdate, UserPublicOut
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("", response_model=list[UserPublicOut])
def get_all_users_public(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(User).filter(User.account_status == 1).all()


@router.get("/me", response_model=UserOut)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.put("/me/password")
def update_password(
    password_data: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not pwd_context.verify(password_data.old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Ancien mot de passe incorrect")

    current_user.password = pwd_context.hash(password_data.new_password)
    db.commit()
    return {"message": "Mot de passe mis à jour avec succès"}


@router.put("/me/update", response_model=UserOut)
def update_profile(
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if profile_data.username is not None:
        existing = db.query(User).filter(
            User.username == profile_data.username,
            User.id_user != current_user.id_user
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Ce username est déjà pris")
        current_user.username = profile_data.username

    if profile_data.location is not None:
        current_user.location = profile_data.location

    db.commit()
    db.refresh(current_user)
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