from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from app import database, models, crud
from fastapi import HTTPException, Depends, status
from fastapi.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from app.schemas import authSchema
import os
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Authorization")


# Verifing JWT token
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# Hashing the password
def hash_password(password: str):
    return pwd_context.hash(password)


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


# Creating JWT token function
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Decode token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise Exception
    except Exception as e:
        raise Exception
    return payload


# Get Current User
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:
    credentials_exception = HTTPException(
        401, "Could not validate credentials", {"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user


# Authorization Middleware
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check for the authorization header
        token = request.headers.get("Authorization")
        if token:
            try:
                # Extract the token from the Authorization header
                token = token.split(" ")[1]  # Remove 'Bearer ' part
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_email = payload.get("sub")
                if user_email:
                    # You can load the user object from the database
                    db = database.SessionLocal()  # Get DB session
                    user = (
                        db.query(models.User)
                        .filter(models.User.email == user_email)
                        .first()
                    )
                    if user:
                        # Attach the user to the request object
                        request.state.user = user
            except JWTError:
                raise HTTPException(status_code=401, detail="Invalid token")
            except Exception as e:
                raise HTTPException(500, f"Internal server error: {str(e)}")
        response = await call_next(request)
        return response
