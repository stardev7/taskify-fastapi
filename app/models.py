from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String)
    
    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    due_date = Column(DateTime, default=datetime.now(timezone.utc))
    completed = Column(Boolean, default=False)
    owner_email = Column(String, ForeignKey("users.email"))
    
    owner = relationship("User", back_populates="tasks")