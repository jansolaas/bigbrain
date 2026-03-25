from typing import Optional

from pydantic import BaseModel, ConfigDict


class SequenceBase(BaseModel):
    project_id: int
    episode_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    is_active: bool = True

class SequenceCreate(SequenceBase):
    """Schema for creating a sequence."""
    pass


class SequenceOut(SequenceBase):
    """Schema for reading a sequence."""
    id: int

    model_config = ConfigDict(from_attributes=True)