from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from models import User, File as FileModel, Upload
from schemas import FileOut
from services.crypto import encrypt_file, decrypt_file
import uuid, os

router    = APIRouter()
UPLOAD_DIR = "storage/"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=FileOut)
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Lire le contenu du fichier
    content = file.file.read()

    # Chiffrer
    encrypted_content = encrypt_file(content)

    # Nom unique sur le disque
    secure_name = f"{uuid.uuid4()}.enc"
    file_path   = os.path.join(UPLOAD_DIR, secure_name)

    # Sauvegarder sur le disque
    with open(file_path, "wb") as f:
        f.write(encrypted_content)

    # Enregistrer en base
    new_file = FileModel(
        file_name=file.filename,
        secure_name=secure_name,
        file_size=len(content),
        mime_type=file.content_type
    )
    db.add(new_file)
    db.flush()  # pour avoir l'id_file avant le commit

    # Lier le fichier à l'utilisateur
    new_upload = Upload(
        id_user=current_user.id_user,
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
    # Vérifier que le fichier existe
    file = db.query(FileModel).filter(FileModel.id_file == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="Fichier introuvable")

    # Vérifier que c'est bien son fichier
    upload = db.query(Upload).filter(
        Upload.id_file == file_id,
        Upload.id_user == current_user.id_user
    ).first()
    if not upload:
        raise HTTPException(status_code=403, detail="Accès refusé")

    # Lire et déchiffrer
    file_path = os.path.join(UPLOAD_DIR, file.secure_name)
    with open(file_path, "rb") as f:
        encrypted_content = f.read()

    decrypted_content = decrypt_file(encrypted_content)

    return Response(
        content=decrypted_content,
        media_type=file.mime_type,
        headers={"Content-Disposition": f"attachment; filename={file.file_name}"}
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