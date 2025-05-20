from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from core.security import create_access_token, verify_password
from ..crud import user as crud_user
from ..schemas.token import Token
from ..schemas.user import UserCreate


router = APIRouter()


@router.post('/register', response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Email already registered'
        )
    user_in = crud_user.create_user(db, user=user)
    access_token = create_access_token(data={'sub': user_in.email})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/login', response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}
