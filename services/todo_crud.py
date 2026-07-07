# services/todo_crud.py
from sqlalchemy.orm import Session
import models
import schemas

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    """Read multiple todos"""
    return db.query(models.Todo).offset(skip).limit(limit).all()

def get_todo(db: Session, todo_id: int):
    """Read a single todo"""
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

def create_todo(db: Session, todo: schemas.TodoCreate):
    """Create a new todo"""
    db_todo = models.Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate):
    """Update an existing todo"""
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo:
        update_data = todo.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    """Delete a todo"""
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo