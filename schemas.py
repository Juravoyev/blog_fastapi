from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class BlogBase(BaseModel):
    author_name: str = Field(max_length=100)
    title: str = Field(max_length=100)
    body: str = Field()

class BlogCreate(BlogBase):
    published_at: datetime
    pass

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    author_name: Optional[str] = None
    body: Optional[str] = None
    published_at: Optional[datetime] = None


class BlogOut(BlogBase):
    id: int

    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)