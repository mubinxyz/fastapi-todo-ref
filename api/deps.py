# api/deps.py
from database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    """Yields a database session and ensures it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()