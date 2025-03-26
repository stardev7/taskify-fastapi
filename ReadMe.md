
# Taskify - Smart Task Management API

## Overview
Taskify is a backend API for a task management system built using FastAPI. It provides users with the ability to create, manage, and track their tasks efficiently. The project is designed with scalability and real-time features using Redis and Celery.

## Features
- 🛠️ **User Authentication** (JWT-based authentication)
- ✅ **Task Management** (Create, update, delete tasks)
- 🏷️ **Task Categories & Labels**
- 🔴 **Priority Levels** (High, Medium, Low)
- ⏰ **Due Dates & Reminders**
- 🔗 **Task Sharing** (Assign tasks to users)
- 📊 **Progress Tracking** (Pending, In-Progress, Completed)

## Tech Stack
- 🚀 **FastAPI** - Web framework for high-performance APIs
- 🗃️ **PostgreSQL** - Relational database
- 🧰 **SQLAlchemy** - ORM for database interactions
- 🧪 **Pydantic** - Data validation and serialization
- 🔥 **Redis** - Caching and real-time updates
- 🛠️ **Celery** - Task scheduling and background jobs

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.9+
- PostgreSQL
- Redis

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/taskify.git
   cd taskify
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```sh
   cp .env.example .env
   ```
   Update `.env` with database and Redis credentials.

5. Run database migrations:
   ```sh
   alembic upgrade head
   ```

6. Start the FastAPI server:
   ```sh
   uvicorn main:app --reload
   ```

7. Start Celery worker:
   ```sh
   celery -A tasks worker --loglevel=info
   ```

## API Documentation
After running the server, visit `http://127.0.0.1:8000/docs` for interactive API documentation via Swagger UI.

## License
This project is developed by Lev Makarov.

My Github URL: http://github.com/levmakarov
