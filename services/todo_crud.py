# services/todo_crud.py
from sqlalchemy.orm import Session
import models, schemas

def get_todos(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    # Only fetch todos belonging to this specific user
    return db.query(models.Todo).filter(models.Todo.owner_id == owner_id).offset(skip).limit(limit).all()

def get_todo(db: Session, todo_id: int, owner_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == owner_id).first()

def create_todo(db: Session, todo: schemas.TodoCreate, owner_id: int):
    db_todo = models.Todo(**todo.model_dump(), owner_id=owner_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# update_todo and delete_todo remain mostly the same, but should verify owner_id
def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate, owner_id: int):
    db_todo = get_todo(db, todo_id, owner_id)
    if db_todo:
        update_data = todo.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int, owner_id: int):
    db_todo = get_todo(db, todo_id, owner_id)
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo