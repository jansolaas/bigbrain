from sqlalchemy import Column, Integer, String, Text, Boolean, Float, JSON
from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    code = Column(String, unique=True, index=True, nullable=False)  # short code, e.g. "BB01"
    description = Column(Text, nullable=True)
    root_path = Column(String, nullable=False)  # e.g. "/mnt/projects/BB01"
    fps = Column(Float, nullable=True)
    config = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)

