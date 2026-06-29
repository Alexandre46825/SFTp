from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
from dependencies import get_current_user
from models import User, File as FileModel, Upload
from schemas import FileOut
from services.pgp import encrypt_file_pgp
import uuid, os

router    = APIRouter()
UPLOAD_DIR = "storage/"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/send", response_model=FileOut)
def send_file(
    file: UploadFile = File(...),
    user_id: int = Form(...),
    expiration_date: int = Form(...),
    message: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    receiver = db.query(User).filter(User.id_user == user_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Destinataire introuvable")

    if not receiver.public_key:
        raise HTTPException(status_code=400, detail="Le destinataire n'a pas de clé PGP")

    content = file.file.read()

    encrypted_content = encrypt_file_pgp(
        file_bytes=content,
        recipient_public_key=receiver.public_key,
        recipient_email=receiver.mail,
        tmp_id=f"send_{current_user.id_user}_{user_id}"
    )

    secure_name = f"{uuid.uuid4()}.gpg"
    file_path   = os.path.join(UPLOAD_DIR, secure_name)

    with open(file_path, "wb") as f:
        f.write(encrypted_content)

    new_file = FileModel(
        file_name=file.filename,
        secure_name=secure_name,
        file_size=len(content),
        mime_type=file.content_type,
        expires_at=datetime.utcnow() + timedelta(days=expiration_date),
        message=message,
        id_sender=current_user.id_user
    )
    db.add(new_file)
    db.flush()

    new_upload = Upload(
        id_user=user_id,
        id_file=new_file.id_file
    )
    db.add(new_upload)
    db.commit()
    db.refresh(new_file)

    return new_file


@router.get("/download/{file_id}")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    file = db.query(FileModel).filter(FileModel.id_file == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="Fichier introuvable")

    upload = db.query(Upload).filter(
        Upload.id_file == file_id,
        Upload.id_user == current_user.id_user
    ).first()
    if not upload:
        raise HTTPException(status_code=403, detail="Accès refusé")

    if file.expires_at and file.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Ce fichier a expiré")

    file_path = os.path.join(UPLOAD_DIR, file.secure_name)
    with open(file_path, "rb") as f:
        encrypted_content = f.read()

    return Response(
        content=encrypted_content,
        media_type="application/pgp-encrypted",
        headers={"Content-Disposition": f"attachment; filename={file.file_name}.gpg"}
    )


@router.get("/my-files", response_model=list[FileOut])
def get_my_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    uploads = db.query(Upload).filter(
        Upload.id_user == current_user.id_user
    ).all()

    return [upload.file for upload in uploads]