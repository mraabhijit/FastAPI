import sys
sys.path.append('..')

from starlette.responses import RedirectResponse
from starlette import status

from fastapi import Depends, APIRouter, Form, Request
import models
from database import engine
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from utils import get_db
from .auth import get_current_user, get_password_hash, verify_password
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory='templates')

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str



@router.get('/edit-user', response_class=HTMLResponse)
async def edit_user(request: Request):

    user_data = await get_current_user(request)

    if not user_data:
        return RedirectResponse(
            url='/auth',
            status_code=status.HTTP_302_FOUND
        )
    
    return templates.TemplateResponse("edit-password.html", 
                                          {"request": request,
                                           "user": user_data})


@router.post('/edit-user', response_class=HTMLResponse)
async def edit_user_creds(request: Request,
                          username: str = Form(),
                          password: str = Form(),
                          new_password: str = Form(), 
                          db: Session = Depends(get_db)
                          ):
    
    user = await get_current_user(request)

    if not user:
        return RedirectResponse(
            url='/auth',
            status_code=status.HTTP_302_FOUND
        )
    
    user_data = db.query(models.Users) \
            .filter(models.Users.username == username).first()

    msg = "Invalid Username or Password"

    if user_data:
        if username == user_data.username and verify_password(password, 
                                                        user_data.hashed_password):
            user_data.hashed_password = get_password_hash(new_password)

            db.add(user_data)
            db.commit()

            msg = "Password Updated"
    
    return templates.TemplateResponse("edit-password.html", 
                                      {"request": request, 
                                       "msg": msg, 
                                       "user": user})
