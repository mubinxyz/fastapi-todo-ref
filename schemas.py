# schemas.py
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import List

# --- AUTH SCHEMAS ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

# --- USER SCHEMAS ---
class UserBase(BaseModel):
    email: EmailStr
    role: str = "user" 

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    # SECURITY: We intentionally OMIT 'role' here. 
    # This prevents malicious users from sending {"role": "admin"} to promote themselves!

class UserResponse(UserBase):
    id: int
    todos: List["TodoResponse"] = []
    model_config = ConfigDict(from_attributes=True)

# --- TODO SCHEMAS ---
class TodoBase(BaseModel):
    title: str
    description: str | None = None
    is_completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None

class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    owner_id: int
    model_config = ConfigDict(from_attributes=True)

UserResponse.model_rebuild()