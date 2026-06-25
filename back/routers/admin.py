from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from dependencies import get_admin_user
from models import User, File, Share, Log, BanRecord
from schemas import UserOut, BanRequest, BanRecordOut, RoleUpdate

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
    user.account_status = 3
    db.commit()
    return {"message": "Utilisateur supprimé"}


@router.put("/users/{user_id}/ban", response_model=BanRecordOut)
def ban_user(
    user_id: int,
    ban_data: BanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    user.account_status = 2

    new_ban = BanRecord(
        id_user=user_id,
        id_admin=current_user.id_user,
        reason=ban_data.reason
    )
    db.add(new_ban)
    db.commit()
    db.refresh(new_ban)
    return new_ban


@router.put("/users/{user_id}/unban")
def unban_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    user.account_status = 1

    last_ban = db.query(BanRecord).filter(
        BanRecord.id_user == user_id,
        BanRecord.unbanned_at.is_(None)
    ).order_by(BanRecord.banned_at.desc()).first()

    if last_ban:
        last_ban.unbanned_at = datetime.utcnow()

    db.commit()
    return {"message": "Utilisateur débanni"}


@router.put("/users/{user_id}/role", response_model=UserOut)
def update_user_role(
    user_id: int,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    if user_id == current_user.id_user and not role_data.is_admin:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas retirer vos propres droits admin")

    user.is_admin = role_data.is_admin
    db.commit()
    db.refresh(user)
    return user


@router.get("/users/{user_id}/ban-history", response_model=list[BanRecordOut])
def get_ban_history(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    return db.query(BanRecord).filter(BanRecord.id_user == user_id).all()


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    return {
        "total_users": db.query(User).count(),
        "active_users": db.query(User).filter(User.account_status == 1).count(),
        "banned_users": db.query(User).filter(User.account_status == 2).count(),
        "deleted_users": db.query(User).filter(User.account_status == 3).count(),
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