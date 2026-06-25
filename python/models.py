from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id_user        = Column(Integer, primary_key=True, index=True)
    name           = Column(String(50))
    surname        = Column(String(50))
    username       = Column(String(50), unique=True, index=True)
    mail           = Column(String(100), unique=True, index=True)
    password       = Column(String(200))
    password_pgp   = Column(String(200), nullable=True)
    location       = Column(String(100), nullable=True)
    account_status = Column(Integer, default=1)
    is_admin       = Column(Boolean, default=False)
    created_at     = Column(DateTime, default=datetime.datetime.utcnow)
    last_login     = Column(DateTime, nullable=True)
    public_key     = Column(Text, nullable=True)
    private_key    = Column(Text, nullable=True)

    uploads          = relationship("Upload", back_populates="user")
    sent_shares      = relationship("Share", foreign_keys="Share.id_sender", back_populates="sender")
    recv_shares      = relationship("Share", foreign_keys="Share.id_receiver", back_populates="receiver")
    logs             = relationship("Log", back_populates="user")
    friendships_sent = relationship("Friendship", foreign_keys="Friendship.id_requester", back_populates="requester")
    friendships_recv = relationship("Friendship", foreign_keys="Friendship.id_receiver", back_populates="receiver")
    ban_records      = relationship("BanRecord", foreign_keys="BanRecord.id_user", back_populates="user")


class Friendship(Base):
    __tablename__ = "friendships"

    id_friendship = Column(Integer, primary_key=True, index=True)
    id_requester  = Column(Integer, ForeignKey("users.id_user"))
    id_receiver   = Column(Integer, ForeignKey("users.id_user"))
    status        = Column(String(20), default="pending")
    created_at    = Column(DateTime, default=datetime.datetime.utcnow)

    requester = relationship("User", foreign_keys=[id_requester], back_populates="friendships_sent")
    receiver  = relationship("User", foreign_keys=[id_receiver], back_populates="friendships_recv")


class File(Base):
    __tablename__ = "files"

    id_file     = Column(Integer, primary_key=True, index=True)
    file_name   = Column(String(255))
    secure_name = Column(String(255), unique=True)
    file_size   = Column(BigInteger)
    mime_type   = Column(String(100))
    upload_at   = Column(DateTime, default=datetime.datetime.utcnow)

    upload = relationship("Upload", back_populates="file")
    shares = relationship("Share", back_populates="file")
    logs   = relationship("Log", back_populates="file")


class Upload(Base):
    __tablename__ = "uploads"

    id_upload   = Column(Integer, primary_key=True, index=True)
    id_user     = Column(Integer, ForeignKey("users.id_user"))
    id_file     = Column(Integer, ForeignKey("files.id_file"))
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="uploads")
    file = relationship("File", back_populates="upload")


class Share(Base):
    __tablename__ = "shares"

    id_share        = Column(Integer, primary_key=True, index=True)
    id_file         = Column(Integer, ForeignKey("files.id_file"))
    id_sender       = Column(Integer, ForeignKey("users.id_user"))
    id_receiver     = Column(Integer, ForeignKey("users.id_user"))
    shared_at       = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at      = Column(DateTime)
    is_downloaded   = Column(Boolean, default=False)
    download_count  = Column(Integer, default=0)
    encryption_type = Column(String(20), default="AES-256")
    message         = Column(Text, nullable=True)

    file     = relationship("File", back_populates="shares")
    sender   = relationship("User", foreign_keys=[id_sender], back_populates="sent_shares")
    receiver = relationship("User", foreign_keys=[id_receiver], back_populates="recv_shares")


class Log(Base):
    __tablename__ = "logs"

    id_log        = Column(Integer, primary_key=True, index=True)
    id_user       = Column(Integer, ForeignKey("users.id_user"), nullable=True)
    id_file       = Column(Integer, ForeignKey("files.id_file"), nullable=True)
    action_type   = Column(String(50))
    ip_address    = Column(String(45))
    log_timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="logs")
    file = relationship("File", back_populates="logs")


class BanRecord(Base):
    __tablename__ = "ban_records"

    id_ban      = Column(Integer, primary_key=True, index=True)
    id_user     = Column(Integer, ForeignKey("users.id_user"))
    id_admin    = Column(Integer, ForeignKey("users.id_user"))
    banned_at   = Column(DateTime, default=datetime.datetime.utcnow)
    unbanned_at = Column(DateTime, nullable=True)
    reason      = Column(String(255))

    user  = relationship("User", foreign_keys=[id_user], back_populates="ban_records")
    admin = relationship("User", foreign_keys=[id_admin])