from fastapi import FastAPI
from enum import Enum
from typing import Union, Optional

app = FastAPI()


BOOKS = {
    'book_1': {'title': "Title One", 'author': "Author One"},
    'book_2': {'title': "Title Two", 'author': "Author Two"},
    'book_3': {'title': "Title Three", 'author': "Author Three"},
    'book_4': {'title': "Title Four", 'author': "Author Four"},
    'book_5': {'title': "Title Five", 'author': "Author Five"},
}


class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"


@app.get('/')
async def read_all_books():
    return BOOKS


# @app.get("/books/{book_id}")
# async def read_book(book_id: int):
#     return {"book_title": book_id}

@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"direction": direction_name, "sub": 'Up'}
    if direction_name == DirectionName.south:
        return {"direction": direction_name, "sub": 'Down'}
    if direction_name == DirectionName.west:
        return {"direction": direction_name, "sub": 'Left'}
    return {"direction": direction_name, "sub": "Right"}
    

@app.get("/books/mybook")
async def read_favorite_book():
    return {"book_title": "My Favourite Book"}

# Query Parameter
@app.get("/books")
async def get_books(skip_book: Optional[str] = None):
    if skip_book: 
        NEW_BOOK = BOOKS.copy()
        del NEW_BOOK[skip_book]
        return NEW_BOOK
    return BOOKS


# Assignment Q1. Create a new read book function that uses query params instead of path params.
@app.get('/booksquery')
async def read_query_book(book_id: int):
    book_name = f'book_{book_id}'
    return BOOKS.get(book_name, 
                     f'Book: {book_name} not found.')


# Parameterized calls should be placed below non-parametrized calls
# Otherwise the path to the get request would think that the parameter is required.

@app.get("/{book_name}")
async def read_book_by_name(book_name: str):
    return BOOKS.get(book_name, 'Book not in database')


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    return {"book_title": book_id}

# Post request to add new entry
@app.post("/")
async def create_book(book_title: str, book_author: str):
    current_book_idx = 0

    if len(BOOKS) > 0:
        for book in BOOKS:
            idx = int(book.split('_')[-1])
            if idx > current_book_idx:
                current_book_idx = idx
    
    BOOKS[f'book_{current_book_idx + 1}'] = {'title': book_title, 'author': book_author}
    return BOOKS.get(f'book_{current_book_idx+1}', 'No Book Added')


# Put request to update entries
@app.put('/{book_name}')
async def update_book(book_name: str, 
                      book_title: str,
                      book_author: str):
    if book_name in BOOKS:
        updated_book_information = {'title': book_title, 'author': book_author}
        BOOKS[book_name] = updated_book_information

        return BOOKS
    
    return f"Invalid Request. Book named {book_name} not found in database. Try adding the book using {create_book}."


# Delete request to remove entry
@app.delete('/{book_name}')
async def delete_book(book_name: str):
    if book_name in BOOKS:
        del BOOKS[book_name]

        return f'Book: {book_name} deleted.'
    
    return f'Book: {book_name} not found.'


# Assignment 2. Create a new delete book function that uses query params instead of path params.
@app.delete('/')
async def delete_book(book_name: str):
    if book_name in BOOKS:
        del BOOKS[book_name]

        return f'Book: {book_name} deleted.'
    
    return f'Book: {book_name} not found.'    
