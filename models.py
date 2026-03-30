from database import Base
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Boolean, Text, func
from sqlalchemy.orm import Mapped, mapped_column

class Blog(Base):
    __tablename__='blogs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_name: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), 
        onupdate=func.now()
    )
    published_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    