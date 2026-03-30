from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from schemas import BlogCreate, BlogOut, BlogUpdate
from database import Base, get_db, engine
from models import Blog
from typing import List


Base.metadata.create_all(bind=engine)
api_router = APIRouter(prefix='/api/blog')

@api_router.get('/', response_model=List[BlogOut])
def get_blogs(db = Depends(get_db)):
    stmt = select(Blog)
    blogs = db.scalars(stmt).all()

    return blogs


@api_router.get('/{blog_id}', response_model=BlogOut)
def get_blog(blog_id: int, db = Depends(get_db)):
    stmt = select(Blog).where(Blog.id == blog_id)
    blog = db.scalar(stmt)

    if not blog:
        raise HTTPException(status_code=404, detail=f"{blog_id}-raqamli blog mavjud emas.")
    return blog

@api_router.post('/', response_model=BlogOut)
def create_blog(blog_in: BlogCreate, db = Depends(get_db)):
    blog = Blog(
        **blog_in.model_dump()
    )

    db.add(blog)
    db.commit()
    db.refresh(blog)

    return blog

@api_router.put('/{blog_id}', response_model=BlogOut)
def update_blog(blog_id: int, blog_in: BlogUpdate, db=Depends(get_db)):
    # 1. Fetch the existing record
    stmt = select(Blog).where(Blog.id == blog_id)
    blog = db.scalar(stmt)

    if not blog:
        raise HTTPException(status_code=404, detail=f"{blog_id}-blog topilmadi.")

    # 2. FIX: Convert the schema to a dictionary of Python objects
    # 'exclude_unset=True' ensures we only update what the user sent
    update_data = blog_in.model_dump(exclude_unset=True)

    # 3. Apply the changes
    for key, value in update_data.items():
        setattr(blog, key, value)

    # 4. Commit and Refresh
    db.commit()
    db.refresh(blog)
    
    return blog


@api_router.delete('/{blog_id}')
def delete_blog(blog_id: int, db = Depends(get_db)):
    stmt = select(Blog).where(Blog.id == blog_id)
    blog = db.scalar(stmt)

    if not blog:
        raise HTTPException(status_code=404, detail=f"{blog_id}-raqamli blog mavjud emas")

    db.delete(blog)
    db.commit()

    return {"status": 204}

