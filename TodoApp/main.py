from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()


# .metdata: MetaData object where newly defined Table objects are collected.
# .create_all(bind=engine): creates all tables stored in this metadata by issuing the appropriate 
# CREATE TABLE statements to the database
# once the following code is executed, a .db file is generated with the provided config
models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Todo(BaseModel):
    description: Optional[str]
    title: str
    priority: int = Field(ge=1, 
                          le=5,
                          description='Priority must be between 1 and 5')
    complete: bool


@app.get('/')
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@app.get('/todo/{todo_id}')
async def read_todo(todo_id: int, 
                    db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos) \
                   .filter(models.Todos.id == todo_id) \
                   .first()
    
    if todo_model:
        return todo_model
    raise http_exception()


@app.post('/')
async def create_todo(todo: Todo, 
                      db: Session = Depends(get_db)):
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model) # places an object to the session. Will be persisted to the db in the next flush operation
    db.commit() # to directly flush the changes

    return successful_response(201)


@app.put('/{todo_id}')
async def update_todo(todo_id: int, 
                      todo: Todo,
                      db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos) \
                   .filter(models.Todos.id == todo_id) \
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


@app.delete('/{todo_id}')
async def delete_todo(todo_id: int,
                      db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos) \
                   .filter(models.Todos.id == todo_id) \
                   .first()
    
    if not todo_model:
        raise http_exception()
    
    db.query(models.Todos) \
      .filter(models.Todos.id == todo_id) \
      .delete()
                 
    db.commit()

    return successful_response(200)


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception():
    raise HTTPException(status_code=404,
                        detail="Todo not found")
