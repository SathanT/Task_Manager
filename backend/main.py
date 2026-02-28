from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging
from typing import List


from . import crud
from . import dbtables as _dbtables  # Ensure models are imported before create_all
from . import schemas
from .database import Base, SessionLocal, engine
from .logging_config import setup_logging


setup_logging()
logger = logging.getLogger(__name__)
Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/getAllTasks/{user_id}", response_model=List[schemas.TaskResponse])
def get_all_task(user_id : int,db: Session = Depends(get_db)):
    try:
        logger.info("request for all task")
        return crud.get_all_tasks(user_id,db)
    except Exception as e:
        logger.warning("user not found")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error while fetching tasks"
        )


@app.put("/markTaskCompleted/{task_id}")
def mark_task_completed(task_id: int,db: Session = Depends(get_db)):
    try:
        logger.info("request for mark task completed")
        crud.mark_task_completed(task_id,db)
        return {"message": "Task marked as completed"}
    except ValueError as e:
        logger.warning("task id not found")
        raise HTTPException(status_code=404, detail=str(e))
    
    
@app.delete("/deleteTask/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        logger.info("request for delete task")
        crud.delete_task(task_id, db)
        return {"message": "Task deleted successfully"}
    except ValueError as e:
        logger.warning("task id not found")
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/createUser", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info("request for create user")
        new_user = crud.create_user(db, user)
        return new_user
    except RuntimeError as e:
        logger.warning("database fetching failed")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/createTask/{user_id}", response_model=schemas.TaskResponse)
def create_task(user_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    try:
        logger.info("request for create task")
        new_task = crud.create_task(db, user_id, task)
        return new_task
    except crud.NotFoundError as e:
        logger.warning("user id not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        logger.warning("database failed")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/validateUser")
def user_validation(user: schemas.UserValidation, db: Session = Depends(get_db)):
    user_found = crud.user_validation(db, user.id, user.email)
    if not user_found:
        logger.warning("user not found %s and %s", user.id, user.email)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    logger.info("user validation success and found %s", user.id)
    return {"exist": True}
