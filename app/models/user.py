# app/models/user.py

from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    tags: List[str] = []

class UserUpdate(BaseModel):
    tags: List[str] = []
