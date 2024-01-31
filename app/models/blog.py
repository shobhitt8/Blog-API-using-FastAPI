# app/models/blog.py

from pydantic import BaseModel
from typing import List

class BlogBase(BaseModel):
    title: str
    content: str
    tags: List[str] = []

class BlogCreate(BlogBase):
    pass

class Blog(BlogBase):
    id: str

class BlogUpdate(BaseModel):
    title: str
    content: str
    tags: List[str] = []
