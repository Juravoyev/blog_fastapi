import jwt
import security

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select
from schemas import BlogCreate, BlogOut, BlogUpdate, AuthorCreate, AuthorOut, Token
from database import get_db
from models import Blog, Author

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession as Session



api_router = APIRouter(prefix='/api/blog')


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token yaroqsiz yoki muddati tugagan"
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    user =  await db.scalar(select(Author).where(Author.id == int(user_id)))
    if user is None:
        raise credentials_exception

    return user


@api_router.post('/authors/login', response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):    
    user = await db.scalar(select(Author).where(Author.username == form.username))
    
    if not user:
        print("Foydalanuvchi topilmadi!")
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud emas")

    print(f"User hashed_password uzunligi: {len(user.hashed_password) if user.hashed_password else 0}")

    if not security.verify_password(form.password, user.hashed_password):
        print("Parol mos kelmadi!")
        raise HTTPException(status_code=400, detail="Username yoki parol noto'g'ri")

    access_token = security.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.get('/{blog_id}', response_model=BlogOut)
async def get_blog(blog_id: int, db = Depends(get_db)):
    stmt = select(Blog).where(Blog.id == blog_id)
    blog = await db.scalar(stmt)

    if not blog:
        raise HTTPException(status_code=404, detail=f"{blog_id}-raqamli blog mavjud emas.")
    return blog


@api_router.post('/authors', response_model=AuthorOut)
async def create_author(author_in: AuthorCreate, db = Depends(get_db)):
    author = await db.scalar(select(Author).where(Author.username == author_in.username))
    if author:
        raise HTTPException(status_code=400, detail=f"{author_in.username}-foydalanuvchi mavjud.")
    
    author_dict = author_in.model_dump()
    hashed_password = security.get_password_hash(author_dict.pop('password'))

    new_author = Author(**author_dict, hashed_password=hashed_password)
    db.add(new_author)
    await db.commit()
    await db.refresh(new_author)

    return new_author


@api_router.post('/', response_model=BlogOut)
async def create_blog(blog_in: BlogCreate, db = Depends(get_db), current_user: Author = Depends(get_current_user)):
    blog_dict = blog_in.model_dump()
    new_blog = Blog(**blog_dict, author_id=current_user.id)
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)

    return new_blog


@api_router.put('/{blog_id}', response_model=BlogOut)
async def update_blog(blog_id: int, blog_in: BlogUpdate, db=Depends(get_db)):
    # 1. Fetch the existing record
    stmt = select(Blog).where(Blog.id == blog_id)
    blog = await db.scalar(stmt)

    if not blog:
        raise HTTPException(status_code=404, detail=f"{blog_id}-blog topilmadi.")

    # 2. FIX: Convert the schema to a dictionary of Python objects
    # 'exclude_unset=True' ensures we only update what the user sent
    update_data = blog_in.model_dump(exclude_unset=True)

    # 3. Apply the changes
    for key, value in update_data.items():
        setattr(blog, key, value)

    # 4. Commit and Refresh
    await db.commit()
    await db.refresh(blog)
    
    return blog


@api_router.delete('/{blog_id}')
async def delete_blog(blog_id: int, db = Depends(get_db)):
    stmt = select(Blog).where(Blog.id == blog_id)
    blog = await db.scalar(stmt)

    if not blog:
        raise HTTPException(status_code=404, detail=f"{blog_id}-raqamli blog mavjud emas")

    db.delete(blog)
    db.commit()

    return {"status": 204}

