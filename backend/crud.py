from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from backend.dbtables import *
from backend.schemas import *

logger = logging.getLogger(__name__)


def create_user(db: Session, user: UserCreate):
    logger.debug("validating user data")

    try:
        new_user = UserDB(name=user.name, email=user.email)
        db.add(new_user)
        db.commit()

        logger.info("user created")

        db.refresh(new_user)
        return new_user
    except Exception as exc:
        # Fixed: rollback transaction and raise explicit API error instead of returning None
        db.rollback()
        logger.exception("user inserting failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        ) from exc


def create_task(db: Session, userid: int, task: TaskCreate):
    user = db.query(UserDB).filter(UserDB.id == userid).first()

    logger.debug("validating user id for task creation")

    if user:
        logger.info("user found")
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

            logger.info("task created for the user")

            return new_task
        except Exception as exc:
            db.rollback()
            logger.exception("task inserting failed")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create task"
            ) from exc
    else:
        logger.exception("database insertion failed user not found")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )


def userValidation(db: Session,userid: int,user_email: str):

    logger.info(f"{userid}{user_email}")
    return db.query(UserDB).filter(UserDB.id == userid , UserDB.email == user_email).first()

    
    
