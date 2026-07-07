# services/user_crud.py
from sqlalchemy.orm import Session
import models, schemas

def get_user_by_email(db: Session, email: str):
    """Fetch a user by their email address."""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    """Create a new user with a securely hashed password."""
    
    # SECURITY FIX: We hardcode role="user" here.
    # Even if a malicious user tries to send {"role": "admin"} in the JSON body,
    # our Pydantic UserCreate schema ignores it, and this service hardcodes it to "user".
    db_user = models.User(
        email=user.email, 
        hashed_password=hashed_password,
        role="user"
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user