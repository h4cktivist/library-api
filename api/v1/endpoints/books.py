from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from api.v1.schemas.user import User
from api.v1.schemas.book import Book, BookCreate, BookUpdate
from api.v1.dependencies.user import get_current_user
from api.v1.crud import book as crud_book


router = APIRouter()


@router.post('/', response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db),
                current_user: str = Depends(get_current_user)):
    return crud_book.create_book(db=db, book=book)


@router.get('/', response_model=List[Book])
def get_books(skip: int = 0,
              limit: int = 100,
              current_user: User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    books = crud_book.get_books(db, skip=skip, limit=limit)
    return books


@router.get('/{book_id}', response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    db_book = crud_book.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
    return db_book


@router.put('/{book_id}', response_model=Book)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db),
                current_user: str = Depends(get_current_user)):
    db_book = crud_book.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
    return crud_book.update_book(db=db, book_id=book_id, book=book)


@router.delete('/{book_id}')
def delete_book(book_id: int, db: Session = Depends(get_db),
                current_user: str = Depends(get_current_user)):
    db_book = crud_book.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
    crud_book.delete_book(db=db, book_id=book_id)
    return {'message': 'Book deleted successfully'}
