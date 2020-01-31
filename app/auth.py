from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends
from jwt import PyJWTError
import jwt

from sqlalchemy.orm import Session

# local import
from . import models, schemas


SECRET_KEY = "b74780a78d1501185f996b87673b87c07e69e280b62f9f89c662214753589b58"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_password_hash(password: str):
    """
    summary: generate password hash

    arguements: (password: str)

    return: hashed password: str
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """
    summary: compare login password with db hashed pass

    arguements: (plain_password: str [password from login]), (hashed_password: str [hash pass from db])

    return: True if match else False
    """
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    """
    summary: basic auth using password and username

    arguments: (db: Session), (username: str), (password: str) 

    return: user if auth info is correct else False
    """
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        return False
    if not verify_password(password, db_user.password):
        return False
    return db_user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """
    summary: create jwt access token 

    arguments: (data: dict), (expires_delta: timedelta)

    return: jwt access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(db: Session, username: str):
    """
    SQL query: SELECT * FROM users WHERE username=username;

    summary: get user by name for get_current_user

    arguments: (db: Session [sqlalchemy database session]), (username: str)

    return: user
    """
    return db.query(models.User).filter(models.User.username == username).first()


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    summary: get currnet auth user

    arguments: (db: Session), (token: str)

    return: current user
    """
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    from .main import database
    user = get_user(db=database.SessionLocal(), username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
