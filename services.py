
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from passlib.context import CryptContext

from schemas import PostCreation, UserCreation
from models import User, Post

hashing = CryptContext(schemes=["bcrypt"], deprecated="auto")
# ----------------------------------------
# USER SERVICES
# ----------------------------------------


def get_user_by_email_service(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id_service(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()


def create_user_service(db: Session, user: UserCreation):
    hashed_password = hashing.hash(user.password)
    new_user = User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users_service(db: Session):
    return db.query(User).all()


# ----------------------------------------
# POST SERVICES
# ----------------------------------------

def create_post_service(db: Session, user_id: int, post: PostCreation):
    new_post = Post(**post.dict(), owner_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_posts_service(db: Session):
    return db.query(Post).all()


def get_post_by_id_service(db: Session, id: int):
    return db.query(Post).filter(Post.id == id).first()


def delete_post_by_id_service(db: Session, id: int):
    db.query(Post).filter(Post.id == id).delete()
    db.commit()


def update_post_by_id_service(db: Session, post_id: int, post: PostCreation):
    
    old_post = get_post_by_id_service(db=db, id=post_id)
    if old_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: '{str(post_id)}' doesn't exists")

    old_post.title = post.title
    old_post.content = post.content
    old_post.updated_at  = datetime.now()
    
    db.commit()
    db.refresh(old_post)

    return old_post

