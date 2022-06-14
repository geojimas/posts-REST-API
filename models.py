from msilib import gen_uuid
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from config import Base


class User (Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255))
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    posts = relationship("Post", back_populates="owner")


class Post (Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), unique=True, index=True)
    content = Column(String(255), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="posts")
