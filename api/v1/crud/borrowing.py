from sqlalchemy.orm import Session
from datetime import datetime

from db.models.borrowing import Borrowing
from db.models.book import Book
from db.models.reader import Reader


def create_borrowing(db: Session, book_id: int, reader_id: int):
    db_borrowing = Borrowing(book_id=book_id, reader_id=reader_id)
    db.add(db_borrowing)
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing


def get_borrowing(db: Session, borrowing_id: int):
    return db.query(Borrowing).filter(Borrowing.id == borrowing_id).first()


def get_active_reader_borrowings(db: Session, reader_id: int):
    return db.query(Borrowing).filter(
        Borrowing.reader_id == reader_id,
        Borrowing.return_date == None
    ).all()


def get_returned_reader_borrowings(db: Session, reader_id: int):
    return db.query(Borrowing).filter(
        Borrowing.reader_id == reader_id,
        Borrowing.return_date is not None
    ).all()


def return_borrowing(db: Session, borrowing_id: int):
    db_borrowing = db.query(Borrowing).filter(
        Borrowing.id == borrowing_id,
        Borrowing.return_date == None
    ).first()

    if db_borrowing:
        db_borrowing.return_date = datetime.utcnow()
        db.commit()
        db.refresh(db_borrowing)

    return db_borrowing


def get_borrowing_by_book_and_reader(db: Session, book_id: int, reader_id: int):
    return db.query(Borrowing).filter(
        Borrowing.book_id == book_id,
        Borrowing.reader_id == reader_id,
        Borrowing.return_date == None
    ).first()
