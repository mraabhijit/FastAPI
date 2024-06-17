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
    
    class Config:
        json_schema_extra = {
            'example': {
                "id": "0298822f-121a-4e77-855f-ce2f149c0c21",
                "title": "Computer Science Pro",
                "author": "mraabhijit",
                "description": "A very nice description of the book",
                "rating": 5
            }
        }


BOOKS = []


@app.get('/')
async def read_all_books(books_to_return: Optional[int] = None):
    if len(BOOKS) < 1:
        create_books_no_api()
    # Add functionality to return a fixed number of books
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i-1])
            i += 1
        return new_books
    return BOOKS


@app.get('/book/{book_id}')
async def read_book(book_id: UUID):
    for book in BOOKS:
        if book_id == book.id:
            return book
    return f'No Book found by UUID: {book_id}' 

@app.post('/')
async def create_book(book: Book):
    BOOKS.append(book)

    return book


@app.put('/{book_id}')
async def update_book(book_id: UUID, 
                      book: Book):
    # counter = 0
    for i, x in enumerate(BOOKS):
        if x.id == book_id:
            BOOKS[i] = book
            return BOOKS[i]


@app.delete('/{book_id}')
async def delete_book(book_id: UUID):
    for i,x in enumerate(BOOKS):
        if x.id == book_id:
            # # if order of books do not matter
            # # can swap the book with last book 
            # # and delete the last book
            # BOOKS[i], BOOKS[-1] = BOOKS[-1], BOOKS[i]
            # BOOKS.pop()

            # if order of books matter
            BOOKS.remove(x)
            return f"ID: {book_id} deleted."
    return f"ID: {book_id} not found."


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



















