import sys
sys.path.append('..')

from fastapi import APIRouter, Depends
import models
from typing import Optional
from database import engine
from sqlalchemy.orm import session
from pydantic import BaseModel
from .auth import get_current_user, get_user_exception
from utils import get_db, successful_response


class Address(BaseModel):
    address1: str
    address2: Optional[str]
    city: str
    state: str
    country: str
    postalcode: str
    apt_num: Optional[int]


models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix = "/address",
    tags=["address"],
    responses={404: 
               {'description': 'Not Found'}} 
)


@router.post('/')
async def create_address(address: Address,
                         user: dict = Depends(get_current_user),
                         db: session = Depends(get_db)):
    if not user:
        raise get_user_exception()
    
    address_model = models.Address()

    address_model.address1 = address.address1
    address_model.address2 = address.address2
    address_model.city = address.city
    address_model.state = address.state
    address_model.country = address.country
    address_model.postalcode = address.postalcode
    address_model.apt_num = address.apt_num

    db.add(address_model)
    db.flush() # Similar to commit but additionally also creates the id

    user_model = db.query(models.Users) \
                   .filter(models.Users.id == user.get('id')) \
                   .first()
    
    user_model.address_id = address_model.id

    db.add(user_model)
    db.commit()

    return successful_response(201)


