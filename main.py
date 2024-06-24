from fastapi import FastAPI, Depends
import models
from database import engine
from routers import auth, todos, users, address
from company import companyapis, dependencies


app = FastAPI()


# .metdata: MetaData object where newly defined Table objects are collected.
# .create_all(bind=engine): creates all tables stored in this metadata by issuing the appropriate 
# CREATE TABLE statements to the database
# once the following code is executed, a .db file is generated with the provided config
models.Base.metadata.create_all(bind=engine)


# include auth, todos route functionalities in main
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(address.router)
app.include_router(
    companyapis.router,
    prefix="/companyapis",
    tags=["companyapis"],
    dependencies=[Depends(dependencies.get_token_header)],
    responses={418: {"description": "Internal Use Only"}}
) # external routing added here to not give the companyapis their own prefix and tags.
app.include_router(users.router)