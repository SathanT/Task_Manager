from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import crud
import dbtables  # Ensure models are imported before create_all
import schemas
from database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.post("/task/{userID}",response_model=schemas.TaskResponse)
def create_task(userID:int,task : schemas.TaskCreate,db:Session=Depends(get_db)):
    return crud.create_task(db,userID,task)