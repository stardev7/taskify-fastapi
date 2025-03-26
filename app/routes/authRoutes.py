from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app import auth, crud
from app.schemas import authSchema
from app.database import get_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Authorization")

@router.post("/register", response_model=authSchema.User)
def register_user(user: authSchema.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(400, "Email already registered")

        hashed_password = auth.hash_password(user.password)
        
        new_user = crud.create_user(db, user, hashed_password)
    except Exception as e:
        raise HTTPException(500, f"Internal server error: {str(e)}")
    return new_user


@router.post("/login", response_model=authSchema.LoginResult)
def login_user(user: authSchema.Login, db: Session = Depends(get_db)):
    try:
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user is None or not auth.verify_password(
            user.password, db_user.password
        ):
            raise HTTPException(
                401, "Invalid credential", {"WWW-Authenticate": "Bearer"}
            )
        access_token = auth.create_access_token(
            data={"sub": user.email},
            expires_delta=auth.timedelta(
                hours=1
            ),  # You can change the expiration time
        )
    except Exception as e:
        raise HTTPException(500, f"Internal server error: {str(e)}")

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify_login", response_model=authSchema.LoginTokenVerify)
def verify_login(token: str = Depends(oauth2_scheme)):
    try:
        result = auth.decode_token(token)
    except Exception as e:
        return {"sub": "Not authorized", "exp": 0}
    return result