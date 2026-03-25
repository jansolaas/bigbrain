from typing import Optional
from pydantic import BaseModel, ConfigDict

# Import Enums from models so we share the definition
from app.models.tasks import TaskType, TaskStatus


class TaskBase(BaseModel):
    name: str
    task_type: TaskType
    status: TaskStatus = TaskStatus.NOT_STARTED
    description: Optional[str] = None
    assignee_id: Optional[int] = None

    # Linkage (one should be set)
    asset_id: Optional[int] = None
    shot_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskOut(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)