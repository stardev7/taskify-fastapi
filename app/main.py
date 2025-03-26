from fastapi import FastAPI, Depends, HTTPException, status
from app.routes import authRoutes, taskRoutes
from app.auth import AuthMiddleware

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Taskify API"}

app.include_router(authRoutes.router, prefix="/auth", tags=["auth"])

app.include_router(taskRoutes.router, prefix="/tasks", tags=["tasks"])
