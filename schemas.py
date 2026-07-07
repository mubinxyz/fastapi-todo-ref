# schemas.py
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional, List

# --- USER SCHEMAS ---
class UserBase(BaseModel):
    email: EmailStr # Pydantic automatically validates this is a real email format!

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    todos: List["TodoResponse"] = [] # Include their todos in the response

    model_config = ConfigDict(from_attributes=True)

# --- TODO SCHEMAS ---
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    owner_id: int # Every todo belongs to a user

    model_config = ConfigDict(from_attributes=True)

# Update forward references (required because User and Todo schemas reference each other)
UserResponse.model_rebuild()