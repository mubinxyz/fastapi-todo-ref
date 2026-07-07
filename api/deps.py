# api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database import SessionLocal
from core.config import settings
import models, schemas

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# This tells Swagger UI where to send the login request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_admin_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized. Admin access required.")
    return current_user