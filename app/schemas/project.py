from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, List


# --- New Strict Config Models ---

class SoftwareConfig(BaseModel):
    maya: Optional[str] = None
    nuke: Optional[str] = None
    houdini: Optional[str] = None
    # You can add validation here, e.g., regex for version numbers


class EnvConfig(BaseModel):
    OCIO: Optional[str] = None
    JOB: Optional[str] = None
    # Allow extra env vars
    extra_vars: Dict[str, str] = Field(default_factory=dict)


class ProjectConfig(BaseModel):
    software: SoftwareConfig = Field(default_factory=SoftwareConfig)
    env: EnvConfig = Field(default_factory=EnvConfig)
    resolution: List[int] = Field(default=[1920, 1080])
    framerate: float = 24.0


# --- Updated Project Schemas ---

class ProjectBase(BaseModel):
    name: str
    code: str
    root_path: str
    description: Optional[str] = None
    fps: Optional[float] = None

    # CHANGE THIS: Use the strict ProjectConfig instead of generic Dict
    config: Optional[ProjectConfig] = Field(default_factory=ProjectConfig)

    is_active: bool = True


class ProjectCreate(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: int
    model_config = ConfigDict(from_attributes=True)