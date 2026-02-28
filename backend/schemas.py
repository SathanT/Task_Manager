from pydantic import BaseModel, ConfigDict, model_validator

from .Task import Priority, TaskStatus


class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class UserValidation(BaseModel):
    id: int
    email: str


class TaskCreate(BaseModel):
    name: str
    description: str
    duration: str
    priority: Priority = Priority.LOW
    status: TaskStatus = TaskStatus.PENDING

class TaskResponse(BaseModel):
    id: int
    name: str
    description: str
    duration: str | None = None
    priority: str
    status: str

    model_config = ConfigDict(from_attributes=True)
