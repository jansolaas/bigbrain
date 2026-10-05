import enum
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from app.database import Base

class DepartmentType(str, enum.Enum):
    MODELING = "modeling"
    RIGGING = "rigging"
    LAYOUT = "layout"
    ANIMATION = "animation"
    FX = "fx"
    LIGHTING = "lighting"
    COMPOSITING = "compositing"


class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True, index=True)

    # A task usually belongs to EITHER an Asset OR a Shot
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True)
    shot_id = Column(Integer, ForeignKey("shots.id"), nullable=True)

    # Assignee (optional)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Core task info
    name = Column(String, index=True, nullable=False)  # e.g. "Animation"
    department_type = Column(Enum(DepartmentType), index=True, nullable=False)
    description = Column(Text, nullable=True)