from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from db.models.base import Base

class Borrowing(Base):
    __tablename__ = 'borrowings'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    reader_id = Column(Integer, ForeignKey('readers.id'), nullable=False)
    borrow_date = Column(DateTime, server_default=func.now())
    return_date = Column(DateTime)
