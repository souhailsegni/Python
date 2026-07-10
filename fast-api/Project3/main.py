from fastapi import FastAPI, Depends, HTTPException, status  # Import HTTPException and status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class todo_request(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=1, le=5)
    complete: bool = False
    owner_id: int = Field(ge=1)
    


# 1. Fetch all todos
@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()

# 2. Fetch a specific todo by its ID
@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    # Query the database for a todo matching the provided ID
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    
    # If it exists, return it
    if todo_model is not None:
        return todo_model
    
    # If it doesn't exist, raise a 404 error
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Todo with ID {todo_id} not found."
    )
    
@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request: todo_request, db: Session = Depends(get_db)):
    todo_model = models.Todos(**todo_request.dict())
    db.add(todo_model)
    db.commit()
    return todo_model

@app.put("/todo/{todo_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_todo(todo_id: int, todo_request: todo_request, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Todo with ID {todo_id} not found."
        )
    
    for key, value in todo_request.dict().items():
        setattr(todo_model, key, value)
    
    db.commit()
    return todo_model

@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Todo with ID {todo_id} not found."
        )
    
    db.delete(todo_model)
    db.commit()
    return {"detail": f"Todo with ID {todo_id} has been deleted."}