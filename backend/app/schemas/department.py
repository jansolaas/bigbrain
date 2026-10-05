from typing import Optional
from pydantic import BaseModel, ConfigDict

# Import Enums from models so we share the definition
from app.models.departments import DepartmentType


class DepartmentBase(BaseModel):
    name: str
    department_type: DepartmentType
    description: Optional[str] = None
    assignee_id: Optional[int] = None

    # Linkage (one should be set)
    asset_id: Optional[int] = None
    shot_id: Optional[int] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentOut(DepartmentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)