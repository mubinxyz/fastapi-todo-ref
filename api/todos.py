# api/todos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.deps import get_db, get_current_user
from services import todo_crud
import schemas, models

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post("/", response_model=schemas.TodoResponse, status_code=201)
def create_todo(
    todo: schemas.TodoCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # Extracts user from token!
):
    return todo_crud.create_todo(db=db, todo=todo, owner_id=current_user.id)

@router.get("/", response_model=list[schemas.TodoResponse])
def read_todos(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return todo_crud.get_todos(db, owner_id=current_user.id, skip=skip, limit=limit)

@router.put("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(
    todo_id: int, 
    todo: schemas.TodoUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_todo = todo_crud.update_todo(db, todo_id=todo_id, todo=todo, owner_id=current_user.id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found or not owned by you")
    return db_todo

@router.delete("/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_todo = todo_crud.delete_todo(db, todo_id=todo_id, owner_id=current_user.id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found or not owned by you")