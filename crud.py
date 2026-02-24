from sqlalchemy.orm import Session
from fastapi import HTTPException,status
import logging

from dbtables import *
from schemas import *

logger=logging.getLogger(__name__)

def create_user(db: Session, user: UserCreate):

    logger.debug("validating user data")

    try:
        new_user = UserDB(name=user.name, email=user.email)
        db.add(new_user)
        db.commit()

        logger.info("user created")

        db.refresh(new_user)
        return new_user
    except Exception:
        logger.exception("user inserting failed")

def create_task(db: Session ,userid:int, task: TaskCreate):
    user=db.query(UserDB).filter(UserDB.id==userid).first()

    logger.debug("validating user id for task creation")

    if user:

        logger.info("user found")

        new_task=TaskDB(
            name=task.name,
            description=task.description,
            priority=task.priority,
            user_id=userid
            )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        logger.info("task created for the user")

        return new_task
    else:

        logger.exception("database insertion failed user not found")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
