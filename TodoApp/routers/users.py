import sys
sys.path.append('..')


from fastapi import APIRouter, Depends
import models
from database import engine
from pydantic import BaseModel
from sqlalchemy.orm import Session
from utils import get_db, successful_response, http_exception
from .auth import (get_current_user, 
                   get_user_exception, 
                   verify_password, 
                   get_password_hash)


# Create a new route within the routers directory called users.py
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not Found"}}
)

models.Base.metadata.create_all(bind=engine)


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str 


# Enhance users.py to be able to return all users within the application
@router.get('/')
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


# Enhance users.py to be able to get a single user by a path parameter
@router.get('/user/{user_id}')
async def user_by_path(user_id: int,
                       db: Session = Depends(get_db)):
    user_model = db.query(models.Users) \
             .filter(models.Users.id == user_id) \
             .first()
    
    if not user_model:
        raise get_user_exception()
    
    return user_model


# Enhance users.py to be able to get a single user by a query parameter
@router.get('/user')
async def user_by_query(user_id: int,
                        db: Session = Depends(get_db)):
    user_model = db.query(models.Users) \
             .filter(models.Users.id == user_id) \
             .first()
    
    if not user_model:
        raise get_user_exception()
    
    return user_model


# Enhance users.py to be able to modify their current user's password, 
# if passed by authentication
@router.put('/user/updatepassword')
async def update_user_password(user_verification: UserVerification,
                               user: dict = Depends(get_current_user),
                               db: Session = Depends(get_db)):
    if not user:
        raise get_user_exception()
    
    user_model = db.query(models.Users) \
                 .filter(models.Users.id == user.get('id')) \
                 .first()

    if not user_model:
        raise http_exception()
    if (user_model.username == user_verification.username) \
        and verify_password(user_verification.password, user_model.hashed_password):

        hash_password = get_password_hash(user_verification.new_password)

        user_model.hashed_password = hash_password
    
        db.add(user_model)
        db.commit()

    return successful_response(status_code=201)


# Enhance users.py to be able to delete their own user.
@router.delete('/user/delete')
async def delete_user(user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if not user:
        raise get_user_exception()
    
    user_model = db.query(models.Users) \
                   .filter(models.Users.id == user.get('id')) \
                   .first()
    
    if not user_model:
        raise http_exception()
    
    db.query(models.Users) \
      .filter(models.Users.id == user.get('id')) \
      .delete()
    
    db.commit()

    return successful_response(200)
                   