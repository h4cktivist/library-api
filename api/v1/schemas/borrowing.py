from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class BorrowingBase(BaseModel):
    book_id: int = Field(..., gt=0)
    reader_id: int = Field(..., gt=0)


class BorrowingCreate(BorrowingBase):
    pass


class BorrowingReturn(BaseModel):
    borrowing_id: int = Field(..., gt=0)


class BorrowingUpdate(BaseModel):
    return_date: Optional[datetime] = Field(None)


class BorrowingInDBBase(BorrowingBase):
    id: int
    borrow_date: datetime
    return_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class Borrowing(BorrowingInDBBase):
    pass


class ReaderBorrowings(BaseModel):
    active_borrowings: list[Borrowing]
    returned_borrowings: list[Borrowing]
