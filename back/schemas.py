from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    name: str
    surname: str
    username: str
    mail: EmailStr
    password: str
    password_pgp: str
    location: Optional[str] = None

class UserOut(BaseModel):
    id_user: int
    name: str
    surname: str
    username: str
    mail: str
    location: Optional[str]
    account_status: int
    is_admin: bool
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True

class UserPublicOut(BaseModel):
    id_user: int
    mail: str
    username: str
    location: Optional[str]

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    mail: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class SenderInfo(BaseModel):
    id_user: int
    name: str
    surname: str
    username: str
    mail: str

    class Config:
        from_attributes = True

class FileOut(BaseModel):
    id_file: int
    file_name: str
    file_size: int
    mime_type: str
    upload_at: datetime
    expires_at: Optional[datetime] = None
    message: Optional[str] = None
    sender: Optional[SenderInfo] = None

    class Config:
        from_attributes = True


class FriendshipCreate(BaseModel):
    id_receiver: int

class FriendshipOut(BaseModel):
    id_friendship: int
    id_requester: int
    id_receiver: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class LogOut(BaseModel):
    id_log: int
    id_user: Optional[int]
    id_file: Optional[int]
    action_type: str
    ip_address: str
    log_timestamp: datetime

    class Config:
        from_attributes = True


class BanRequest(BaseModel):
    reason: str

class BanRecordOut(BaseModel):
    id_ban: int
    id_user: int
    id_admin: int
    banned_at: datetime
    unbanned_at: Optional[datetime]
    reason: str

    class Config:
        from_attributes = True


class RoleUpdate(BaseModel):
    is_admin: bool


class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str

class ProfileUpdate(BaseModel):
    username: Optional[str] = None
    location: Optional[str] = None