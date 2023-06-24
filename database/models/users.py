from typing import Optional
from sqlmodel import SQLModel, Field
import bcrypt


class UserBase(SQLModel):
    username: str
    login: str
    password: str


class Users(UserBase, table=True):
    id: Optional[int] = Field(primary_key=True)

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


class UserLogin(SQLModel):
    login: str
    password: str


class UserReg(UserBase):
    pass


class UserRead(UserBase):
    id: int
