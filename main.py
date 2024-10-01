# main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal, engine
import models
import schemas
from sqlalchemy.orm import joinedload

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve HTML file
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/api_interface.html", "r") as f:
        return f.read()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/posts", response_model=List[schemas.PostWithRelations])
def read_posts(
    status: Optional[str] = None,
    include: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    query = db.query(models.Post)
    
    if status:
        query = query.filter(models.Post.status == status)
    
    if include:
        relations = include.split(',')
        for relation in relations:
            if relation == 'tags':
                query = query.options(joinedload(models.Post.tags))
            elif relation == 'user':
                query = query.options(joinedload(models.Post.user))
    
    posts = query.offset(skip).limit(limit).all()
    return posts

@app.get("/api/posts/{post_id}", response_model=schemas.PostWithRelations)
def read_post(
    post_id: int,
    include: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Post)
    
    if include:
        relations = include.split(',')
        for relation in relations:
            if relation == 'tags':
                query = query.options(joinedload(models.Post.tags))
            elif relation == 'user':
                query = query.options(joinedload(models.Post.user))
            elif relation == 'comments':
                query = query.options(joinedload(models.Post.comments))
    
    post = query.filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.get("/api/users/{user_id}", response_model=schemas.UserWithRelations)
def read_user(
    user_id: int,
    include: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.User)
    
    if include:
        relations = include.split(',')
        for relation in relations:
            if relation == 'posts':
                query = query.options(joinedload(models.User.posts))
            elif relation == 'comments':
                query = query.options(joinedload(models.User.comments))
    
    user = query.filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)