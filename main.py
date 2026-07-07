# main.py
from fastapi import FastAPI
from database import engine, Base
from api import todos, users

# 1. Create tables
Base.metadata.create_all(bind=engine)

# 2. Initialize App
app = FastAPI(
    title="Level-Up Todo API",
    description="A highly structured, scalable FastAPI application."
)

# 3. Register Routers
app.include_router(users.router)
app.include_router(todos.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the fastapi Todo API!"}