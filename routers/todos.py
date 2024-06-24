import sys
sys.path.append('..')


from fastapi import Depends, APIRouter
import models
from database import engine
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional
from utils import get_db, successful_response, http_exception
from .auth import get_current_user, get_user_exception


router = APIRouter(
    prefix="/todos", # all api of todo.py with start with /todo prefix
    tags=["todos"], # all api of todo.py will be clubbed under tag todo
    responses={404: {"description": "Not found"}} # a default response
)


# .metdata: MetaData object where newly defined Table objects are collected.
# .create_all(bind=engine): creates all tables stored in this metadata by issuing the appropriate 
# CREATE TABLE statements to the database
# once the following code is executed, a .db file is generated with the provided config
models.Base.metadata.create_all(bind=engine)


class Todo(BaseModel):
    description: Optional[str]
    title: str
    priority: int = Field(ge=1, 
                          le=5,
                          description='Priority must be between 1 and 5')
    complete: bool


@router.get('/')
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@router.get('/{todo_id}')
async def read_todo(todo_id: int, 
                    user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if not user:
        raise get_user_exception()

    todo_model = db.query(models.Todos) \
                   .filter(models.Todos.id == todo_id) \
                   .filter(models.Todos.owner_id == user.get('id')) \
                   .first()
    
    if todo_model:
        return todo_model
    raise http_exception()


@router.get('/user')
async def read_all_by_user(user: dict = Depends(get_current_user), 
                           db: Session = Depends(get_db)):
    if not user:
        raise get_user_exception()
    return db.query(models.Todos) \
             .filter(models.Todos.owner_id == user.get('id')) \
             .all()


@router.post('/')
async def create_todo(todo: Todo, 
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if not user:
        raise get_user_exception()
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get('id')

    db.add(todo_model) # places an object to the session. Will be persisted to the db in the next flush operation
    db.commit() # to directly flush the changes

    return successful_response(201)


@router.put('/{todo_id}')
async def update_todo(todo_id: int, 
                      todo: Todo,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    
    if not user:
        raise get_user_exception()
    
    todo_model = db.query(models.Todos) \
                   .filter(models.Todos.id == todo_id) \
                   .filter(models.Todos.owner_id == user.get('id')) \
                   .first()
    
    if not todo_model:
        raise http_exception()

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    return successful_response(200)


@router.delete('/{todo_id}')
async def delete_todo(todo_id: int,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if not user:
        raise get_user_exception()
    
    todo_model = db.query(models.Todos) \
                   .filter(models.Todos.owner_id == user.get('id')) \
                   .filter(models.Todos.id == todo_id) \
                   .first()
    
    if not todo_model:
        raise http_exception()
    
    db.query(models.Todos) \
      .filter(models.Todos.owner_id == user.get('id')) \
      .filter(models.Todos.id == todo_id) \
      .delete()
                 
    db.commit()

    return successful_response(200)