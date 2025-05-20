from sqlalchemy import Column, Integer, String
from db.models.base import Base


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer)
    isbn = Column(String, unique=True)
    quantity = Column(Integer, default=1, nullable=False)
    description = Column(String)
