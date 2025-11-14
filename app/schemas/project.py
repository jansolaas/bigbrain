from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProjectBase(BaseModel):
    name: str
    code: str
    root_path: str
    description: Optional[str] = None
    fps: Optional[float] = None
    is_active: bool = True


class ProjectCreate(ProjectBase):
    """Schema for creating a project."""
    pass


class ProjectOut(ProjectBase):
    """Schema for reading a project."""
    id: int

    model_config = ConfigDict(from_attributes=True)