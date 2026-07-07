# schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Base schema with shared properties
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False

# Schema for creating a Todo (inherits from Base)
class TodoCreate(TodoBase):
    pass

# Schema for updating a Todo (all fields optional for partial updates)
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

# Schema for returning data to the user
class TodoResponse(TodoBase):
    id: int
    created_at: datetime

    # Pydantic V2 state-of-the-art configuration to read SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)