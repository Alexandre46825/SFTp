from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from dependencies import get_admin_user
from models import User, File, Log, BanRecord
from schemas import UserOut, BanRequest, BanRecordOut, RoleUpdate
import os

router = APIRouter()

UPLOAD_DIR = "storage/"


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
    }


@router.get("/overview")
def get_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    total_users = db.query(User).count()

    files_sent = db.query(Log).filter(
        Log.action_type.like("file_sent_to_%")
    ).count()

    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    uploads_today = db.query(Log).filter(
        Log.action_type.like("file_sent_to_%"),
        Log.log_timestamp >= today_start
    ).count()

    storage_used_bytes = 0
    if os.path.exists(UPLOAD_DIR):
        for filename in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, filename)
            if os.path.isfile(file_path):
                storage_used_bytes += os.path.getsize(file_path)

    storage_used_gb = round(storage_used_bytes / (1024 ** 3), 2)

    return {
        "total_users": total_users,
        "files_sent": files_sent,
        "uploads_today": uploads_today,
        "storage_used_gb": storage_used_gb,
        "storage_used_bytes": storage_used_bytes
    }


@router.get("/logs")
def get_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    logs = db.query(Log).order_by(Log.log_timestamp.desc()).limit(100).all()
    return logs