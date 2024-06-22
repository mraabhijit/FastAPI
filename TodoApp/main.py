from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos


app = FastAPI()


# .metdata: MetaData object where newly defined Table objects are collected.
# .create_all(bind=engine): creates all tables stored in this metadata by issuing the appropriate 
# CREATE TABLE statements to the database
# once the following code is executed, a .db file is generated with the provided config
models.Base.metadata.create_all(bind=engine)


# include auth, todos route functionalities in main
app.include_router(auth.router)
app.include_router(todos.router)