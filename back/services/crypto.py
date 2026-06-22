from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

AES_KEY = os.getenv("AES_KEY")
cipher  = Fernet(AES_KEY.encode())

def encrypt_file(data: bytes) -> bytes:
    return cipher.encrypt(data)

def decrypt_file(data: bytes) -> bytes:
    return cipher.decrypt(data)