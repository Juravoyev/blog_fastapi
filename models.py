from database import Base
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Boolean, Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Author(Base):
    __tablename__='authors'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(length=50), unique=True)
    first_name: Mapped[str] = mapped_column(String(length=100))
    last_name: Mapped[str] = mapped_column(String(length=100))

    blogs: Mapped[List["Blog"]] = relationship(back_populates='author')

    hashed_password: Mapped[str]= mapped_column(String(length=200))
    commented: Mapped[bool] = mapped_column(Boolean, default=False)
    likes: Mapped[int] = mapped_column(Integer, default=0)

class Blog(Base):
    __tablename__='blogs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    body: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship(back_populates="blogs")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), 
        onupdate=func.now()
    )
    published_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    
