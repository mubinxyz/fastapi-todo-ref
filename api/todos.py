# api/todos.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from api.deps import get_db
from services import todo_crud
import schemas

router = APIRouter(
    prefix="/todos", # All routes here will automatically start with /todos
    tags=["Todos"]   # Groups these endpoints beautifully in the /docs UI
)

@router.post("/", response_model=schemas.TodoResponse, status_code=201)
def create_todo(
    todo: schemas.TodoCreate, 
    db: Session = Depends(get_db),
    # For testing, we will pass owner_id as a query parameter. 
    # Later, you will replace this with a real OAuth2 Token dependency!
    owner_id: int = Query(..., description="The ID of the user creating the todo")
):
    return todo_crud.create_todo(db=db, todo=todo, owner_id=owner_id)

@router.get("/", response_model=list[schemas.TodoResponse])
def read_todos(
    owner_id: int = Query(...),
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return todo_crud.get_todos(db, owner_id=owner_id, skip=skip, limit=limit)

@router.put("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(
    todo_id: int, 
    todo: schemas.TodoUpdate, 
    owner_id: int = Query(...),
    db: Session = Depends(get_db)
):
    db_todo = todo_crud.update_todo(db, todo_id=todo_id, todo=todo, owner_id=owner_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.delete("/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int, 
    owner_id: int = Query(...),
    db: Session = Depends(get_db)
):
    db_todo = todo_crud.delete_todo(db, todo_id=todo_id, owner_id=owner_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")