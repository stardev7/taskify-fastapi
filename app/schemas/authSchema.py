from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True

class Login(BaseModel):
    email: str
    password: str

class LoginResult(BaseModel):
    access_token: str
    token_type: str
    
class LoginTokenVerify(BaseModel):
    sub: str
    exp: int

class User(UserBase):
    email: str

    class Config:
        orm_mode = True
