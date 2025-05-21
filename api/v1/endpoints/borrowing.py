from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from api.v1.crud import (
    book as crud_book,
    reader as crud_reader,
    borrowing as crud_borrowing
)
from api.v1.dependencies.user import get_current_user
from api.v1.schemas.borrowing import BorrowingCreate, BorrowingReturn, ReaderBorrowings


router = APIRouter()


@router.post('/borrow')
def borrow_book(
        borrowing: BorrowingCreate,
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)
):
    db_book = crud_book.get_book(db, book_id=borrowing.book_id)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')

    db_reader = crud_reader.get_reader(db, reader_id=borrowing.reader_id)
    if not db_reader:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Reader not found')

    if db_book.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No available copies of this book')

    active_borrowings = crud_borrowing.get_active_reader_borrowings(db, reader_id=borrowing.reader_id)
    if len(active_borrowings) >= 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Reader has reached the maximum number of borrowed books (3)'
        )

    existing_borrowing = crud_borrowing.get_borrowing_by_book_and_reader(
        db,
        book_id=borrowing.book_id,
        reader_id=borrowing.reader_id
    )
    if existing_borrowing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Reader already has this book'
        )

    crud_book.decrease_book_quantity(db, book_id=borrowing.book_id)
    db_borrowing = crud_borrowing.create_borrowing(
        db,
        book_id=borrowing.book_id,
        reader_id=borrowing.reader_id
    )

    db.commit()
    return {
        'message': 'Book borrowed successfully',
        'borrowing_id': db_borrowing.id
    }


@router.post('/return')
def return_book(
        borrowing: BorrowingReturn,
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)
):
    db_borrowing = crud_borrowing.get_borrowing(db, borrowing_id=borrowing.borrowing_id)
    if not db_borrowing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Borrowing record not found')

    if db_borrowing.return_date is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This book has already been returned')

    db_book = crud_book.get_book(db, book_id=db_borrowing.book_id)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')

    crud_book.increase_book_quantity(db, book_id=db_book.id)
    crud_borrowing.return_borrowing(db, borrowing_id=borrowing.borrowing_id)

    db.commit()
    return {'message': 'Book returned successfully'}


@router.get('/reader/{reader_id}', response_model=ReaderBorrowings)
def get_reader_borrowings(reader_id: int, db: Session = Depends(get_db),
                          current_user: str = Depends(get_current_user)):
    return {
        'active_borrowings': crud_borrowing.get_active_reader_borrowings(db, reader_id=reader_id),
        'returned_borrowings': crud_borrowing.get_returned_reader_borrowings(db, reader_id=reader_id)
    }
