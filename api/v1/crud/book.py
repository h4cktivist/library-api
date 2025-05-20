from sqlalchemy.orm import Session
from typing import Optional
from db.models.book import Book
from api.v1.schemas.book import BookCreate, BookUpdate


def get_book(db: Session, book_id: int) -> Optional[Book]:
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100) -> list[type[Book]]:
    return db.query(Book).offset(skip).limit(limit).all()


def get_book_by_isbn(db: Session, isbn: str) -> Optional[Book]:
    return db.query(Book).filter(Book.isbn == isbn).first()


def create_book(db: Session, book: BookCreate) -> Book:
    db_book = Book(
        title=book.title,
        author=book.author,
        year=book.year,
        isbn=book.isbn,
        quantity=book.quantity if book.quantity is not None else 1,
        description=book.description
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: BookUpdate) -> Optional[Book]:
    db_book = get_book(db, book_id=book_id)
    if db_book:
        update_data = book.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_book, field, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> Optional[Book]:
    db_book = get_book(db, book_id=book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book


def decrease_book_quantity(db: Session, book_id: int) -> Optional[Book]:
    db_book = get_book(db, book_id=book_id)
    if db_book and db_book.quantity > 0:
        db_book.quantity -= 1
        db.commit()
        db.refresh(db_book)
    return db_book


def increase_book_quantity(db: Session, book_id: int) -> Optional[Book]:
    db_book = get_book(db, book_id=book_id)
    if db_book:
        db_book.quantity += 1
        db.commit()
        db.refresh(db_book)
    return db_book
