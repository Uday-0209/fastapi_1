from fastapi import APIRouter, Depends, HTTPException, status, Path
from database import  SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos, users
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/users',
    tags = ['users']
)

class UserVerification(BaseModel):
    password:str
    new_password:str = Field(min_length=6)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#This line is used in FastAPI to inject a database session into route functions
db_D = Annotated[Session, Depends(get_db)]
user_D = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user:user_D, db:db_D):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(users).filter(users.id == user.get('id')).first()

@router.put('/password', status_code=status.HTTP_200_OK)
async def change_password(user:user_D, db:db_D, 
                          user_verification:UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(users).filter(users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put('/phone_number/{phone_number}', status_code=status.HTTP_200_OK)
async def add_number(user:user_D, db:db_D, 
                     phone_number:str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(users).filter(users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()

