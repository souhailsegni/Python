from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import models
from routers import auth, todos
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)