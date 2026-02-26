from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException, status
import logging

import crud
import dbtables  # Ensure models are imported before create_all
import schemas
from database import Base, SessionLocal, engine
from logging_config import setup_logging

setup_logging()
logger=logging.getLogger(__name__)
Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/createUser", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.post("/createTask/{userID}",response_model=schemas.TaskResponse)
def create_task(userID:int,task : schemas.TaskCreate,db:Session=Depends(get_db)):
    return crud.create_task(db,userID,task)

@app.post("/validateUser")
def uservaliidation(user: schemas.UserValidation,db :Session=Depends(get_db)):
    user_found=crud.userValidation(db,user.id,user.email)
    if not user_found:
        logger.warning(f"user not found {user.id} and {user.email}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    logger.info(f"user validation seccuss and found {user.id}")
    return {"exist": True}