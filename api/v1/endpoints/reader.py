from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from api.v1.schemas.reader import Reader, ReaderCreate, ReaderUpdate
from api.v1.crud import reader as crud_reader
from api.v1.dependencies.user import get_current_user


router = APIRouter()


@router.post('/', response_model=Reader)
def create_reader(
    reader: ReaderCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    try:
        return crud_reader.create_reader(db=db, reader=reader)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', response_model=List[Reader])
def read_readers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return crud_reader.get_readers(db, skip=skip, limit=limit)


@router.get('/{reader_id}', response_model=Reader)
def read_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_reader = crud_reader.get_reader(db, reader_id=reader_id)
    if db_reader is None:
        raise HTTPException(status_code=404, detail='Reader not found')
    return db_reader


@router.put('/{reader_id}', response_model=Reader)
def update_reader(
    reader_id: int,
    reader: ReaderUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_reader = crud_reader.get_reader(db, reader_id=reader_id)
    if db_reader is None:
        raise HTTPException(status_code=404, detail='Reader not found')
    return crud_reader.update_reader(db=db, reader_id=reader_id, reader=reader)


@router.delete('/{reader_id}')
def delete_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_reader = crud_reader.get_reader(db, reader_id=reader_id)
    if db_reader is None:
        raise HTTPException(status_code=404, detail='Reader not found')
    crud_reader.delete_reader(db=db, reader_id=reader_id)
    return {'message': 'Reader deleted successfully'}
