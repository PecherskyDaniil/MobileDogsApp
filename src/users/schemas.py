from pydantic import BaseModel

class UserBase(BaseModel):
    nickname: str
    email: str
    phone: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    token:str
    class Config:
        orm_mode = True