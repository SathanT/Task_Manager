from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db_url = ""
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
