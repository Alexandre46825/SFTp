from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from models import User, File, Share, Upload
from schemas import ShareCreate, ShareOut
from services.crypto import decrypt_file
from datetime import datetime, timedelta
import os

router = APIRouter()


@router.post("/send", response_model=ShareOut)
def send_file(
    share_data: ShareCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Vérifier que le fichier existe
    file = db.query(File).filter(File.id_file == share_data.id_file).first()
    if not file:
        raise HTTPException(status_code=404, detail="Fichier introuvable")

    # Vérifier que c'est bien son fichier
    upload = db.query(Upload).filter(
        Upload.id_file == share_data.id_file,
        Upload.id_user == current_user.id_user
    ).first()
    if not upload:
        raise HTTPException(status_code=403, detail="Ce fichier ne vous appartient pas")

    # Vérifier que le destinataire existe
    receiver = db.query(User).filter(User.id_user == share_data.id_receiver).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Destinataire introuvable")

    # Vérifier qu'on s'envoie pas à soi-même
    if share_data.id_receiver == current_user.id_user:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas vous envoyer un fichier à vous-même")

    # Créer le partage
    new_share = Share(
        id_file=share_data.id_file,
        id_sender=current_user.id_user,
        id_receiver=share_data.id_receiver,
        expires_at=datetime.utcnow() + timedelta(days=share_data.expires_days),
        encryption_type=share_data.encryption_type,
        message=share_data.message
    )
    db.add(new_share)
    db.commit()
    db.refresh(new_share)
    return new_share


@router.get("/received", response_model=list[ShareOut])
def get_received_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    shares = db.query(Share).filter(
        Share.id_receiver == current_user.id_user,
        Share.expires_at > datetime.utcnow()
    ).all()
    return shares


@router.get("/sent", response_model=list[ShareOut])
def get_sent_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    shares = db.query(Share).filter(
        Share.id_sender == current_user.id_user
    ).all()
    return shares


@router.get("/download/{share_id}")
def download_shared_file(
    share_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Vérifier que le share existe et appartient au receiver
    share = db.query(Share).filter(
        Share.id_share == share_id,
        Share.id_receiver == current_user.id_user
    ).first()
    if not share:
        raise HTTPException(status_code=404, detail="Partage introuvable")

    # Vérifier expiration
    if share.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Ce lien a expiré")

    # Lire et déchiffrer
    file_path = os.path.join("storage/", share.file.secure_name)
    with open(file_path, "rb") as f:
        encrypted_content = f.read()

    decrypted_content = decrypt_file(encrypted_content)

    # Mettre à jour les stats
    share.download_count += 1
    share.is_downloaded = True
    db.commit()

    return Response(
        content=decrypted_content,
        media_type=share.file.mime_type,
        headers={"Content-Disposition": f"attachment; filename={share.file.file_name}"}
    )