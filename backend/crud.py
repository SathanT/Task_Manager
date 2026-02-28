from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging

from .dbtables import TaskDB, UserDB
from .schemas import TaskCreate, UserCreate

logger = logging.getLogger(__name__)

class NotFoundError(Exception):
    """Custom exception for not found entities"""
    pass

def mark_task_completed(task_id: int,db : Session):
        logger.info("task completion request")
        task = db.query(TaskDB).filter(TaskDB.id==task_id).first()
        if not task:
            logger.debug("task not found")
            raise ValueError("Task not found")
        task.status="Completed"
        logger.info("marked task as completed")
        db.commit()
        db.refresh(task)
        return task


def delete_task(task_id: int, db: Session):
    logger.info("task deletion request")
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        logger.debug("task not found")
        raise ValueError("Task not found")
    logger.info("task deleted")
    db.delete(task)
    db.commit()


def get_all_tasks(user_id: int,db: Session):
    try:
        logger.info("get all task request")
        tasks = db.query(TaskDB).filter(TaskDB.user_id == user_id).all()
        logger.info("query success return tasks")
        return tasks
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching tasks: {str(e)}")
        raise


def create_user(db: Session, user: UserCreate):
    logger.debug("Validating user data")
    try:
        new_user = UserDB(name=user.name, email=user.email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"User created with id: {new_user.id}")
        return new_user

    except Exception as exc:
        db.rollback()
        logger.exception("Failed to insert user")
        raise RuntimeError("Database error during user creation") from exc


def create_task(db: Session, userid: int, task: TaskCreate):
    user = db.query(UserDB).filter(UserDB.id == userid).first()
    if not user:
        logger.warning(f"User with id {userid} not found")
        raise NotFoundError("User not found")

    logger.debug(f"Creating task for user {userid}")
    try:
        new_task = TaskDB(
            name=task.name,
            description=task.description,
            duration=task.duration,
            priority=task.priority,
            status=task.status,
            user_id=userid
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        logger.info(f"Task created with id: {new_task.id} for user {userid}")
        return new_task

    except Exception as exc:
        db.rollback()
        logger.exception("Failed to insert task")
        raise RuntimeError("Database error during task creation") from exc


def user_validation(db: Session, userid: int, user_email: str):
    logger.debug(f"Validating user id={userid}, email={user_email}")
    return db.query(UserDB).filter(UserDB.id == userid, UserDB.email == user_email).first()



# Backward-compatible aliases for old call sites.
get_All_Tasks = get_all_tasks
userValidation = user_validation
