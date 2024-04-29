from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nickname=Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone=Column(String, unique=True, index=True)
    hashed_password = Column(String)
    token=Column(String)
