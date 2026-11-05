from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str = ""


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

    model_config = {"from_attributes": True}



