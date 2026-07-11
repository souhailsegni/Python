from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import models
from database import SessionLocal
from .auth import get_current_user

# 1. Initialize the router instead of the FastAPI app
router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

user_dependency = Annotated[models.Users, Depends(get_current_user)]

class todo_request(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=1, le=5)
    complete: bool = False
    
# 2. Use @router for all your endpoints
# Fetch all todos
@router.get("/")
async def read_all(user: user_dependency, db: Session = Depends(get_db)):
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()

# Fetch a specific todo by its ID
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, todo_id: int, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()
    
    if todo_model is not None:
        return todo_model
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Todo with ID {todo_id} not found."
    )
    
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo( 
                      user: user_dependency,
                      todo_request: todo_request,
                      db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    todo_model = models.Todos(**todo_request.dict(), owner_id=user.get("id"))
    db.add(todo_model)
    db.commit()

@router.put("/todo/{todo_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_todo(user: user_dependency, todo_id: int, todo_request: todo_request, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()
    
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Todo with ID {todo_id} not found."
        )
    
    for key, value in todo_request.dict().items():
        setattr(todo_model, key, value)
    
    db.commit()
    return todo_model

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, todo_id: int, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()
    
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Todo with ID {todo_id} not found."
        )
    
    db.delete(todo_model)
    db.commit()
    return {"detail": f"Todo with ID {todo_id} has been deleted."}