from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class ReaderBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., max_length=100)


class ReaderCreate(ReaderBase):
    pass


class ReaderUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = Field(None, max_length=100)


class Reader(ReaderBase):
    id: int

    class Config:
        from_attributes = True
