from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from main import get_db, successful_response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt


SECRET_KEY = "KlgHdwQudw323130Iklsdf9231sdpetbg8"
ALGORITHM = "HS256"


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# If auth.py is called before main.py
# this will create all the tables and elements
models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')

app = FastAPI()


def get_password_hash(password: str):
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, 
                    hashed_password: str):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str,
                      password: str,
                      db: Session = Depends(get_db)):
    user = db.query(models.Users) \
             .filter(models.Users.username == username) \
             .first()
    
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, 
                        user_id: int, 
                        expires_delta: Optional[timedelta] = None):
    encode = {'sub': username, 
              'id': user_id}
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    encode.update({'exp': expire})

    return jwt.encode(encode, 
                      SECRET_KEY, 
                      algorithm=ALGORITHM)


@app.post('/create/user')
async def create_new_user(create_user: CreateUser, 
                          db: Session = Depends(get_db)):
    create_user_model = models.Users()

    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.first_name = create_user.first_name
    create_user_model.last_name = create_user.last_name

    hash_password = get_password_hash(create_user.password)

    create_user_model.hashed_password = hash_password
    create_user_model.is_active = True

    db.add(create_user_model)
    db.commit()

    return successful_response(status_code=201)


@app.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), 
                                 db: Session = Depends(get_db)):
    user = authenticate_user(username=form_data.username, 
                             password=form_data.password,
                             db=db)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )
    # return "User Validated"
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, 
                                user.id, 
                                expires_delta=token_expires)
    
    return {"token": token}