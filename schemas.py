from pydantic import BaseModel, ConfigDict, model_validator


class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    name: str
    description: str
    duration: str
    priority: str = "LOW"
    status: str = "PENDING"

    @model_validator(mode="after")
    def check(self):
        if len(self.name) < 3 or not self.name.isalpha():
            raise ValueError("name must be alphabetic and at least 3 characters")
        return self


class TaskResponse(BaseModel):
    id: int
    name: str
    priority:str
    status:str
    model_config = ConfigDict(from_attributes=True)
