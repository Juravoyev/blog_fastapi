from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class AuthorBase(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)


class AuthorCreate(AuthorBase):
    pass

class AuthorOut(AuthorBase):
    id: int




class BlogBase(BaseModel):
    title: str = Field(max_length=100)
    body: str = Field()
    author_id: int

class BlogCreate(BlogBase):
    published_at: datetime
    pass

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    author_id: Optional[int] = None
    body: Optional[str] = None
    published_at: Optional[datetime] = None


class BlogOut(BlogBase):
    id: int

    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)