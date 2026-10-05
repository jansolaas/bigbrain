import enum
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
from app.models.projects import Project


class VersionType(enum.Enum):
    IMAGE_STACK = "image_stack"
    ALEMBIC = "alembic"
    SIM = "sim"
    MOV = "mov"
    USD = "usd"
    USDA = "usda"

class VersionDepartments(enum.Enum):
    departments = Project.config.departments

class VersionTasks(enum.Enum):
    tasks = Project.config.tasks



class Version(Base):
    __tablename__ = "versions"

    id = Column(Integer, primary_key=True, index=True)
    version_number = Column(Integer, nullable=False)

    department = Column(Text, nullable=False)
    task = Column(Text, nullable=False)

    file_path = Column(String, nullable=False)   # path to the published file on disk/storage
    comment = Column(Text, nullable=True)
    version_type = Column(Enum(VersionType), nullable=False, default=VersionType.IMAGE_STACK)

    created_at = Column(DateTime(timezone=True), server_default=func.now())