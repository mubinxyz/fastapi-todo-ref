# core/security.py
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import bcrypt # <--- Import bcrypt directly
from core.config import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # bcrypt.checkpw compares the plain text to the stored hash
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

def get_password_hash(password: str) -> str:
    # 1. Convert string to bytes
    pwd_bytes = password.encode('utf-8')
    # 2. Generate a random salt
    salt = bcrypt.gensalt()
    # 3. Hash the password with the salt
    hashed_pwd = bcrypt.hashpw(pwd_bytes, salt)
    # 4. Return as a string to save to the database
    return hashed_pwd.decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt