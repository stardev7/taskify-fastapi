from sqlalchemy.orm import Session
from app import models
from app.schemas import authSchema, taskSchema

def create_user(db: Session, user: authSchema.UserCreate, hashed_password: str):
    db_user = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session):
    return db.query(models.User).all()

# Create task
def create_task(db: Session, task: taskSchema.TaskCreate, user_email: int):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        owner_email=user_email
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Get all tasks for a user
def get_tasks_by_user(db: Session, user_email: int, skip: int = 0, limit: int = 100):
    return db.query(models.Task).filter(models.Task.owner_email == user_email).offset(skip).limit(limit).all()

# Get task by ID
def get_task_by_id(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

# Update task
def update_task(db: Session, task_id: int, task: taskSchema.TaskCreate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db_task.title = task.title
        db_task.description = task.description
        db_task.due_date = task.due_date
        db.commit()
        db.refresh(db_task)
        return db_task
    return None

# Delete task
def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return db_task
    return None