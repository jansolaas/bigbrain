from typing import Optional
from pydantic import BaseModel, ConfigDict

class SoftwareBase(BaseModel):
    name: str
    version: str
    exec_path: Optional[str] = None
    is_active: bool = True

class SoftwareCreate(SoftwareBase):
    pass

class SoftwareOut(SoftwareBase):
    id: int
    model_config = ConfigDict(from_attributes=True)