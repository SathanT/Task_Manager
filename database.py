from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db_url = "mysql+pymysql://root:root%40123@localhost:3306/task_db"
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
