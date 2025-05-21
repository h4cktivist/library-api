import pytest
from fastapi import status
from sqlalchemy.orm import Session

from datetime import datetime, timedelta

from db.models.book import Book
from db.models.reader import Reader
from db.models.borrowing import Borrowing


def test_borrow_book_success(db: Session, client, librarian_token):
    book = Book(title='Test Book', author='Author', quantity=2)
    reader = Reader(name='Test Reader', email='reader@test.com')
    db.add_all([book, reader])
    db.commit()

    response = client.post(
        '/borrowings/borrow',
        json={'book_id': book.id, 'reader_id': reader.id},
        headers={'Authorization': f'Bearer {librarian_token}'}
    )

    assert response.status_code == status.HTTP_200_OK
    assert db.query(Borrowing).count() == 1
    assert db.query(Book).filter(Book.id == book.id).first().quantity == 1


def test_borrow_book_no_copies(db: Session, client, librarian_token):
    book = Book(title='Test Book', author='Author', quantity=0)
    reader = Reader(name='Test Reader', email='reader1@test.com')
    db.add_all([book, reader])
    db.commit()

    response = client.post(
        '/borrowings/borrow',
        json={'book_id': book.id, 'reader_id': reader.id},
        headers={'Authorization': f'Bearer {librarian_token}'}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'No available copies' in response.json()['detail']


def test_borrow_book_max_limit(db: Session, client, librarian_token):
    reader = Reader(name='Test Reader', email='reader2@test.com')
    books = [Book(title=f'Book {i}', author='Author', quantity=1) for i in range(4)]
    db.add_all([reader] + books)
    db.commit()

    for i in range(3):
        client.post(
            '/borrowings/borrow',
            json={'book_id': books[i].id, 'reader_id': reader.id},
            headers={'Authorization': f'Bearer {librarian_token}'}
        )

    response = client.post(
        '/borrowings/borrow',
        json={'book_id': books[3].id, 'reader_id': reader.id},
        headers={'Authorization': f'Bearer {librarian_token}'}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'maximum number' in response.json()['detail']
    assert db.query(Borrowing).filter(Borrowing.return_date.is_(None),
                                      Borrowing.reader_id == reader.id).count() == 3


def test_return_book_success(db: Session, client, librarian_token):
    book = Book(title='Test Book', author='Author', quantity=2)
    reader = Reader(name='Test Reader', email='reader3@test.com')
    db.add_all([book, reader])
    db.commit()

    borrowing_id = client.post(
        '/borrowings/borrow',
        json={'book_id': book.id, 'reader_id': reader.id},
        headers={'Authorization': f'Bearer {librarian_token}'}
    ).json()['borrowing_id']

    response = client.post(
        '/borrowings/return',
        json={'borrowing_id': borrowing_id},
        headers={'Authorization': f'Bearer {librarian_token}'}
    )

    assert response.status_code == status.HTTP_200_OK
    assert db.query(Book).filter(Book.id == book.id).first().quantity == 2
    assert db.query(Borrowing).filter(Borrowing.id == borrowing_id).first().return_date is not None


def test_return_already_returned(db: Session, client, librarian_token):
    book = Book(title='Test Book', author='Author', quantity=1)
    reader = Reader(name='Test Reader', email='reader4@test.com')
    db.add_all([book, reader])
    db.commit()

    borrowing_id = client.post(
        '/borrowings/borrow',
        json={'book_id': book.id, 'reader_id': reader.id},
        headers={'Authorization': f'Bearer {librarian_token}'}
    ).json()['borrowing_id']

    client.post(
        '/borrowings/return',
        json={'borrowing_id': borrowing_id},
        headers={'Authorization': f'Bearer {librarian_token}'}
    )

    response = client.post(
        '/borrowings/return',
        json={'borrowing_id': borrowing_id},
        headers={'Authorization': f'Bearer {librarian_token}'}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'already been returned' in response.json()['detail']


def test_return_nonexistent_borrowing(client, librarian_token):
    response = client.post(
        '/borrowings/return',
        json={'borrowing_id': 999},
        headers={'Authorization': f'Bearer {librarian_token}'}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
