import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from database import Base, get_db
from main import app

load_dotenv()

DATABASE_URL = os.getenv("TEST_DATABASE_URL")


test_engine = create_async_engine(DATABASE_URL,
                       connect_args={'check_same_thread': False},
                       echo=True)

TestSession = async_sessionmaker(bind=test_engine, autoflush=False)

async def override_get_db():
    async with TestSession() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

async def init_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_db())


test_client = TestClient(app)



def test_create_author():
    response = test_client.post("/api/blog/authors", json={
        "username": "testuser",
        "password": "123456",
        "first_name": "Test",
        "last_name": "User"
    })

    assert response.status_code == 200
    data = response.json()

    assert data["first_name"] == "Test"
    assert data["last_name"] == "User"



def test_login():
    response = test_client.post(
        "/api/blog/authors/login",
        data={"username": "testuser", "password": "123456"}
    )

    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None



def test_create_blog():
    token = test_client.post(
        "/api/blog/authors/login",
        data={"username": "testuser", "password": "123456"}
    ).json()["access_token"]

    response = test_client.post(
        "/api/blog/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Blog",
            "body": "Hello world"  
        }
    )

    assert response.status_code == 200


def test_get_blog():
    response = test_client.get("/api/blog/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_update_blog():
    response = test_client.put("/api/blog/1", json={
        "title": "Updated Blog"
    })

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Blog"


def test_delete_blog():
    response = test_client.delete("/api/blog/1")

    assert response.status_code == 200


def test_upload_avatar():
    # login
    token = test_client.post(
        "/api/blog/authors/login",
        data={"username": "testuser", "password": "123456"}
    ).json()["access_token"]

    # fake file
    with open("avatar.jpg", "wb") as f:
        f.write(b"test image content")

    with open("avatar.jpg", "rb") as f:
        response = test_client.post(
            "/api/blog/authors/avatar",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": ("avatar.jpg", f, "image/jpeg")}
        )

    assert response.status_code == 200
    assert "avatar" in response.json()