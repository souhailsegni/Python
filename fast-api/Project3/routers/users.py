from typing import Annotated
from pydantic import Field, BaseModel
from models import Users
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from database import SessionLocal
from .auth import get_current_user, bcrypt_context

router = APIRouter(
    prefix='/users',
    tags=['users']
)



class PasswordChangeRequest(BaseModel):
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/user", status_code=status.HTTP_200_OK)
async def get_user_info(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return user

@router.put("/user/change-password", status_code=status.HTTP_200_OK)
async def change_password(user: user_dependency, db: db_dependency, new_password: PasswordChangeRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found.')
    
    hashed_password = bcrypt_context.hash(new_password.password)
    user_model.hashed_password = hashed_password
    db.commit()
    
    return {"message": "Password changed successfully."}