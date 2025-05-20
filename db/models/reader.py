from sqlalchemy import Column, Integer, String
from db.models.base import Base


class Reader(Base):
    __tablename__ = 'readers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
