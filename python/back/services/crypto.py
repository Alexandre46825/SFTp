from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

AES_KEY = os.getenv("AES_KEY")
cipher  = Fernet(AES_KEY.encode())


def encrypt_text(plain_text: str) -> str:
    if plain_text is None:
        return None
    return cipher.encrypt(plain_text.encode()).decode()


def decrypt_text(encrypted_text: str) -> str:
    if encrypted_text is None:
        return None
    return cipher.decrypt(encrypted_text.encode()).decode()