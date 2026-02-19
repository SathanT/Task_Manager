from sqlalchemy.orm import Session
from fastapi import HTTPException,status

from dbtables import *
from schemas import *


def create_user(db: Session, user: UserCreate):
    new_user = UserDB(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_task(db: Session ,userid:int, task: TaskCreate):
    user=db.query(UserDB).filter(UserDB.id==userid).first()
    if user:
        new_task=TaskDB(
            name=task.name,
            description=task.description,
            priority=task.priority,
            user_id=userid
            )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
