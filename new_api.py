from typing import Optional
from fastapi import FastAPI, Body, Path , Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

ukmh = FastAPI()
class book:
    id:int
    title:str
    author:str
    description:str
    ratings:int
    published_year:int

    def __init__(self,id, title, author, description, ratings, published_year):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.ratings = ratings
        self.published_year = published_year

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed to create', default=None)
    title:str=Field(min_length = 3)
    author:str = Field(min_length=1)
    description:str= Field(min_length=1, max_length=100)
    ratings:int= Field(gt=-1, lt=6)
    published_year:int = Field(gt=2000, lt=2033)

    model_config = {
        'json_schema_extra':{
            'example': {
                'title':'A New Book',
                'author':'My Self',
                'description':'A new age book',
                'ratings': 5,
                'published_year':2021
            }
        }
    }
    


Books = [
    book(1, 'title 1', 'auth 1','good one',4,2022),
    book(2, 'title 2', 'auth 2','good two',3, 2021),
    book(3, 'title 3', 'auth 3','good three',5, 2025),
    book(4, 'title 4', 'auth 4','good four',2, 2005),
    book(5, 'title 5', 'auth 5','good five',4, 2006),
    book(6, 'title 6', 'auth 6','good six',3, 2014),
    book(7, 'title 7', 'auth 7','good seven',5, 2017),
    book(8, 'title 8', 'auth 8','good eight',3, 2032)
]

@ukmh.get('/books', status_code=status.HTTP_200_OK)
async def read_all_books():
    return Books

@ukmh.post('/create_books', status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    #print(type(book_request))
    new_book = book(**book_request.model_dump())
    print(type(new_book))
    Books.append(find_book_id(new_book))

def find_book_id(book: book):
    # if len(Books)>0:
    #     book.id = Books[-1].id+1
    # else:
    #     book.id = 1
    # return book
    '''same can be written in one line'''
    book.id = 1 if len(Books) == 0 else Books[-1].id+1
    return book


@ukmh.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def find_book_by_id(book_id:int = Path(gt=0)):
    for book in Books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')


@ukmh.get('/books/', status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rate:int = Query (gt=0, lt=6)):
    read_book = []
    for book in Books:
        if book.ratings == book_rate:
            read_book.append(book)
    return read_book



@ukmh.put('/books/update_book', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book:BookRequest):
    book_changed = False
    for i in range(len(Books)):
        if Books[i].id == book.id:
            Books[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")
    

@ukmh.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int = Path(gt=0)):
    book_deleted = False
    for i in range(len(Books)):
        if Books[i].id == book_id:
            Books.pop(i)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail='Item Still not deleted')


@ukmh.get('/books/publish/', status_code=status.HTTP_200_OK)
async def read_book_on_published_year(published_year:int = Query(gt=2000, lt=2033)):
    for book in Books:
        if book.published_year == published_year:
            return book