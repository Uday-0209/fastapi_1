from fastapi import APIRouter, Depends, HTTPException, status, Path
from database import  SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos
from pydantic import BaseModel, Field


router = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#This line is used in FastAPI to inject a database session into route functions
db_D = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=50)
    priority: int = Field(gt=0, lt=10)
    complete: bool


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_D):
    return db.query(Todos).all()

@router.get("/todo/{todo_id}", status_code = status.HTTP_200_OK)
async def read_todo(db: db_D, todo_id:int = Path(gt=0)):
    #the first() is filter saves the performance time
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='The todos id is not present')

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def post_to_do(db: db_D, todo_request:TodoRequest):
    todo_model = Todos(**todo_request.dict())

    db.add(todo_model)
    db.commit()

@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_D, todo_request :TodoRequest, todo_id :int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@router.delete('/todo/{todo_id}')
async def delete_todo(db:db_D,todo_request:TodoRequest,todo_id :int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todos not found')
    db.query(Todos).filter(Todos.id == todo_id).delete() 
    db.commit()
    

