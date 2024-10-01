# test_main.py
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base
from models import User, Post, Comment, Tag

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def setup_module(module):
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    
    # Add some test data
    db = TestingSessionLocal()
    user = User(id=1, username="testuser", email="test@example.com")
    post = Post(id=1, title="Test Post", content="This is a test post", status="published", user=user)
    comment = Comment(id=1, content="Test comment", post=post, user=user)
    tag = Tag(id=1, name="test")
    post.tags.append(tag)
    db.add_all([user, post, comment, tag])
    db.commit()
    db.close()

def teardown_module(module):
    # Drop the database
    Base.metadata.drop_all(bind=engine)

def test_read_posts():
    response = client.get("/api/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_posts_with_status():
    response = client.get("/api/posts?status=published")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_read_posts_with_include():
    response = client.get("/api/posts?include=tags,user")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if len(response.json()) > 0:
        assert "tags" in response.json()[0]
        assert "user" in response.json()[0]

def test_read_post():
    response = client.get("/api/posts/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert "title" in response.json()

def test_read_post_with_include():
    response = client.get("/api/posts/1?include=tags,user,comments")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert "tags" in response.json()
    assert "user" in response.json()
    assert "comments" in response.json()

def test_read_nonexistent_post():
    response = client.get("/api/posts/999")
    assert response.status_code == 404

def test_read_user():
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert "username" in response.json()

def test_read_user_with_include():
    response = client.get("/api/users/1?include=posts,comments")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert "posts" in response.json()
    assert "comments" in response.json()

def test_read_nonexistent_user():
    response = client.get("/api/users/999")
    assert response.status_code == 404