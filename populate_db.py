# populate_db.py
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from models import Base
from sqlalchemy.exc import IntegrityError

def get_or_create(db: Session, model, **kwargs):
    instance = db.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        try:
            instance = model(**kwargs)
            db.add(instance)
            db.commit()
            return instance
        except IntegrityError:
            db.rollback()
            return db.query(model).filter_by(**kwargs).first()

def create_dummy_data(db: Session):
    # Create users
    user1 = get_or_create(db, models.User, username="john_doe", email="john@example.com")
    user2 = get_or_create(db, models.User, username="jane_smith", email="jane@example.com")

    # Create tags
    tag1 = get_or_create(db, models.Tag, name="Technology")
    tag2 = get_or_create(db, models.Tag, name="Science")
    tag3 = get_or_create(db, models.Tag, name="Programming")

    # Create posts
    post1 = get_or_create(db, models.Post, 
        title="Introduction to FastAPI",
        content="FastAPI is a modern, fast web framework for building APIs with Python 3.6+",
        status="published",
        user_id=user1.id
    )
    post2 = get_or_create(db, models.Post,
        title="The Future of AI",
        content="Artificial Intelligence is rapidly evolving and shaping our future",
        status="draft",
        user_id=user2.id
    )
    post3 = get_or_create(db, models.Post,
        title="Python Tips and Tricks",
        content="Useful Python tips to enhance your coding skills",
        status="published",
        user_id=user1.id
    )

    # Add tags to posts
    for post, tags in [
        (post1, [tag1, tag3]),
        (post2, [tag1, tag2]),
        (post3, [tag3])
    ]:
        for tag in tags:
            if tag not in post.tags:
                post.tags.append(tag)
    
    db.commit()

    # Create comments
    comment1 = get_or_create(db, models.Comment,
        content="Great introduction!",
        post_id=post1.id,
        user_id=user2.id
    )
    comment2 = get_or_create(db, models.Comment,
        content="Looking forward to the final version",
        post_id=post2.id,
        user_id=user1.id
    )
    comment3 = get_or_create(db, models.Comment,
        content="Very helpful, thanks!",
        post_id=post3.id,
        user_id=user2.id
    )

    db.commit()
    print("Database populated with dummy data")

def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        create_dummy_data(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()