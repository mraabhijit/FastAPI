from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Union, Optional
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return: int):
        self.books_to_return = books_to_return

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


# Create No Rating class to mimic the behaviour of 
# responding only with Username, when user logs in
# with Username and Password
class BookNoRating(BaseModel):
    id: UUID 
    title: str = Field(min_length=1) 
    author: str = Field(min_length=1, 
                        max_length=100)
    description: Optional[str] = Field(
        None, 
        title='Description of the book', 
        min_length=1,
        max_length=100)


BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request,
                                            exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Hey, why do you want {exception.books_to_return} "
                            f"books? You need to read more!"}
    )


@app.post('/books/login')
async def book_login(username: str = Form(),
                     password: str = Form()):
    return {'username': username,
            'password': password}


USERNAME: str = 'FastAPIUser'
PASSWORD: str = 'test1234!'
@app.post('/header/login')
async def book_login(book_id: int, 
                     username: Optional[str] = Header(None),
                     password: Optional[str] = Header(None)):
    if username == USERNAME and password == PASSWORD:
        if book_id > 0 and book_id <= len(BOOKS):
            return BOOKS[book_id-1] 
        raise raise_item_cannot_be_found_exception()
    return 'Invalid User'


@app.get('/header')
async def read_header(random_header: Optional[str] = Header(None)):
    return {'Random-Header': random_header}


@app.get('/')
async def read_all_books(books_to_return: Optional[int] = None):

    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)

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
    raise raise_item_cannot_be_found_exception()


# When the function is called, the books will be read from Books class
# However when the function returns book, FastAPI will automatically
# convert it's output data to it's type declaration which is BookNoRating
# and correctly interpret and limit the output data
@app.get('/book/rating/{book_id}', response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for book in BOOKS:
        if book_id == book.id:
            return book
    raise raise_item_cannot_be_found_exception()


# Change default status code to reflect entity creation
@app.post('/', status_code=status.HTTP_201_CREATED)
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
    raise raise_item_cannot_be_found_exception()


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
    raise raise_item_cannot_be_found_exception()


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


def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404,
                         detail="Book not found",
                         headers={'X-Header-Error':
                                  "Nothing to be seen at the UUID"})
















