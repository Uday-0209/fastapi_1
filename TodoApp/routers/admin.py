from fastapi import APIRouter, Depends, HTTPException, status, Path
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Todos
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags = ['admin']
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#This line is used in FastAPI to inject a database session into route functions
db_D = Annotated[Session, Depends(get_db)]
user_D = Annotated[dict, Depends(get_current_user)]


@router.get('/todo', status_code=status.HTTP_200_OK)
async def read_all(user:user_D, db:db_D):
    if user is None or user.get('user_role')!= 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).all()

@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_D, db:db_D, todo_id:int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()