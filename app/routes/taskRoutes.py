from fastapi import APIRouter, Depends, HTTPException
from app import crud, models
from app.database import get_db
from app.auth import get_current_user
from app.schemas import taskSchema
from sqlalchemy.orm import Session

router = APIRouter()

# Create task
@router.post("/", response_model=taskSchema.Task)
def create_task(
    task: taskSchema.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    return crud.create_task(db=db, task=task, user_email=current_user.email)

# Get all tasks for current user
@router.get("/", response_model=list[taskSchema.Task])
def get_tasks(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    tasks = crud.get_tasks_by_user(db=db, user_email=current_user.email, skip=skip, limit=limit)
    return tasks

# Get task by ID
@router.get("/{task_id}", response_model=taskSchema.Task)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = crud.get_task_by_id(db=db, task_id=task_id)
    if task is None or task.owner_email != current_user.email:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Update task
@router.put("/{task_id}", response_model=taskSchema.Task)
def update_task(
    task_id: int, task: taskSchema.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    updated_task = crud.update_task(db=db, task_id=task_id, task=task)
    if updated_task is None or updated_task.owner_email != current_user.email:
        raise HTTPException(status_code=404, detail="Task not found or not owned by current user")
    return updated_task

# Delete task
@router.delete("/{task_id}", response_model=taskSchema.Task)
def delete_task(
    task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    task = crud.delete_task(db=db, task_id=task_id)
    if task is None or task.owner_email != current_user.email:
        raise HTTPException(status_code=404, detail="Task not found or not owned by current user")
    return task