import hashlib
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Ключ для кук
COOKIE_SECRET = Fernet.generate_key()
fernet = Fernet(COOKIE_SECRET)

# Параметры Diffie-Hellman (Группа 14)
P = int("FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74"
        "020BBEA63B139B22514A08798E34041", 16)
G = 2

def encrypt_cookie(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_cookie(data: str) -> str:
    return fernet.decrypt(data.encode()).decode()

def derive_aes_key(shared_secret: int):
    """Превращает число DH в 32-байтный ключ для AES"""
    return hashlib.sha256(str(shared_secret).encode()).digest()

def decrypt_payload(encrypted_data_b64, shared_key):
    """Дешифровка данных от клиента (AES-CBC)"""
    raw_data = base64.b64decode(encrypted_data_b64)
    iv = raw_data[:16]
    cipher = AES.new(shared_key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(raw_data[16:]), AES.block_size)
    return decrypted.decode()