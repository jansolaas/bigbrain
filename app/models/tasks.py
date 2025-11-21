import enum
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from app.database import Base


class TaskType(str, enum.Enum):
    MODELING = "modeling"
    RIGGING = "rigging"
    LAYOUT = "layout"
    ANIMATION = "animation"
    FX = "fx"
    LIGHTING = "lighting"
    COMPOSITING = "compositing"


class TaskStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    OMITTED = "omitted"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    # A task usually belongs to EITHER an Asset OR a Shot
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True)
    shot_id = Column(Integer, ForeignKey("shots.id"), nullable=True)

    # Assignee (optional)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Core task info
    name = Column(String, index=True, nullable=False)  # e.g. "Animation"
    task_type = Column(Enum(TaskType), index=True, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.NOT_STARTED, index=True)
    description = Column(Text, nullable=True)