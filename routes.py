from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.responses import JSONResponse

from config import SessionLocal
from schemas import PostCreation, User, Post, UserCreation
from services import get_user_by_email_service, create_user_service, get_user_by_id_service, get_users_service, create_post_service, get_posts_service, get_post_by_id_service, delete_post_by_id_service, update_post_by_id_service

router = APIRouter(prefix="/api")


# Init ORM
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------------------
# USER ENDPOINTS
# ----------------------------------------


# Return all Users
@router.get('/users', response_model=list[User], status_code=status.HTTP_200_OK)
async def read_users(db: Session = Depends(get_db)):
    users = get_users_service(db=db)

    return users


# Return Specific User
@router.get('/users/{user_id}', response_model=User, status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: Session = Depends(get_db)):

    user = get_user_by_id_service(db=db, id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: '{str(user_id)}' doesn't exists")

    return user


# Create User
@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreation, db: Session = Depends(get_db)):
    db_user = get_user_by_email_service(email=user.email, db=db)

    if (db_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists!")

    user = create_user_service(db=db, user=user)
    return user


# ----------------------------------------
# POST ENDPOINTS
# ----------------------------------------


# Return all Posts
@router.get('/posts', response_model=list[Post], status_code=status.HTTP_200_OK)
async def read_posts(db: Session = Depends(get_db)):
    posts = get_posts_service(db=db)

    return posts


# Return Specific Post
@router.get('/posts/{post_id}', response_model=Post, status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: Session = Depends(get_db)):

    post = get_post_by_id_service(db=db, id=post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: '{str(post_id)}' doesn't exists")

    return post


# Create new Post
@router.post('/users/{user_id}/posts', response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(user_id: int, post: PostCreation, db: Session = Depends(get_db)):
    user = get_user_by_id_service(db=db, id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: '{str(user_id)}' doesn't exists")

    post = create_post_service(db=db, user_id=user_id, post=post)

    return post


# Update specific Post
@router.patch('/posts/{post_id}', response_model=Post, status_code=status.HTTP_200_OK)
async def update_post(post_id: int, post: PostCreation, db: Session = Depends(get_db)):

    return update_post_by_id_service(db=db, post_id=post_id, post=post)


# Delete Post
@router.delete('/posts/{post_id}', status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = get_post_by_id_service(db=db, id=post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: '{str(post_id)}' doesn't exists")

    delete_post_by_id_service(db=db, id=post_id)

    return JSONResponse(content={
        "message": f"Post with id: '{str(post_id)}' deleted Successfully!"
    })
