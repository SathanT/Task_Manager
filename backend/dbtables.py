from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base
from .Task import Priority, TaskStatus



class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))

    tasks = relationship("TaskDB", back_populates="owner", cascade="all, delete")


class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(255))
    duration = Column(String(255))

    priority = Column(Enum(Priority), default=Priority.LOW)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    owner = relationship("UserDB", back_populates="tasks")
