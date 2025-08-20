from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from house_app.db.model import UserProfile ,RefreshToken
from house_app.db.schema import UserProfileCreateSchema ,UserProfileLoginSchema
from house_app.db.database import SessionLocal
from typing import  List, Optional
from house_app.config import SECRET_KEY
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from house_app.config import (SECRET_KEY, REFRESH_TOKEN_LIFETIME,
                              ACCESS_TOKEN_LIFETIME, ALGORITHM)

from datetime import datetime,timedelta
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

auth_router = APIRouter(prefix='/auth' ,tags=['Auth'] )


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: Optional[timedelta]= None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_LIFETIME))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data : dict):
    return create_access_token(data , expires_delta= timedelta(days=REFRESH_TOKEN_LIFETIME))


@auth_router.post('/register', response_model=dict)
async def register(user : UserProfileCreateSchema ,db : Session = Depends(get_db)):

    check_user = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    if check_user:
        raise HTTPException(status_code=404 , detail='Username already...')

    check_email = db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if check_email:
        raise HTTPException(status_code=400, detail='Email already...')

    hash_pass = get_password_hash(user.password)

    user_db = UserProfile(
        first_name = user.first_name,
        last_name = user.last_name,
        username = user.username,
        email = user.email,
        phone_number = user.phone_number,
        role = user.role,
        password = hash_pass,
    )

    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return {'message' : 'успех!'}

@auth_router.post('/login')
async  def login(form_data : UserProfileLoginSchema,
                 db : Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.username == form_data.username).first()
    if not user or not verify_password(form_data.password , user.password):
        raise HTTPException(status_code=401, detail='Error')

    access_token = create_access_token({'sub': user.username})
    refresh_token = create_refresh_token({'sub': user.username})

    new = RefreshToken(user_id = user.id,token = refresh_token)
    db.add(new)
    db.commit()



    return {'access_token' : access_token , 'refresh_token':refresh_token, 'token_type' : 'bearer'}

@auth_router.post('/logout')
async def logout(refresh_token: str,
                 db : Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(status_code=404, detail='Tuura emes')
    db.delete(stored_token)
    db.commit()

    return {'message' : 'Вышли!'}


@auth_router.post('/refresh')
async def refresh(refresh_token: str,
                  db : Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(status_code=404, detail='Маалымат туура эмес!')

    access_token = create_access_token({'sub': stored_token.id})
    return {'access_token' : access_token, 'token_type' : 'bearer'}






