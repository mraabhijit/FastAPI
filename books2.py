from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Union, Optional


app = FastAPI()


class Book(BaseModel):
    id: UUID 
    title: str = Field(min_length=1) # Adding Field to give additional data validation with min length of title
    author: str = Field(min_length=1, 
                        max_length=100)
    description: Optional[str] = Field(title='Description of the book', 
                             min_length=1,
                             max_length=100)
    rating: int = Field(ge=1, 
                        le=5)


BOOKS = []


@app.get('/')
async def read_all_books():
    if len(BOOKS) < 1:
        create_books_no_api()
    return BOOKS


@app.post('/')
async def create_book(book: Book):
    BOOKS.append(book)

    return book


def create_books_no_api():
    book_1 = Book(id = "0298822f-121a-4e77-855f-ce2f149c0c20",
                  title='Title 1',
                  author='Author 1',
                  description='Descrition 1',
                  rating=5)
    book_2 = Book(id = "0498822f-121a-4e77-855f-ce2f149c0c20",
                  title='Title 2',
                  author='Author 2',
                  description='Descrition 2',
                  rating=4)
    book_3 = Book(id = "0698822f-121a-4e77-855f-ce2f149c0c20",
                  title='Title 3',
                  author='Author 3',
                  description='Descrition 3',
                  rating=2)
    book_4 = Book(id = "0998822f-121a-4e77-855f-ce2f149c0c20",
                  title='Title 4',
                  author='Author 4',
                  description='Descrition 4',
                  rating=3)
    BOOKS.extend([book_1, book_2, book_3, book_4])



















