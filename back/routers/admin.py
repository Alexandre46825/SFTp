from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_admin_user
from models import User, File, Share, Log
from schemas import UserOut

router = APIRouter()


@router.get("/users", response_model=list[UserOut])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    return db.query(User).all()


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    db.delete(user)
    db.commit()
    return {"message": "Utilisateur supprimé"}


@router.put("/users/{user_id}/ban")
def ban_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    user.is_active = False
    db.commit()
    return {"message": "Utilisateur banni"}


@router.put("/users/{user_id}/unban")
def unban_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    user.is_active = True
    db.commit()
    return {"message": "Utilisateur débanni"}


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    return {
        "total_users": db.query(User).count(),
        "active_users": db.query(User).filter(User.is_active == True).count(),
        "total_files": db.query(File).count(),
        "total_shares": db.query(Share).count(),
    }


@router.get("/logs")
def get_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    logs = db.query(Log).order_by(Log.log_timestamp.desc()).limit(100).all()
    return logs