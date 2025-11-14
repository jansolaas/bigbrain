from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class Shot(Base):
    __tablename__ = "shots"

    id = Column(Integer, primary_key=True, index=True)

    # Link to projects table
    project_id = Column(Integer, ForeignKey("projects.id"), index=True, nullable=False)

    # Simple identifiers
    name = Column(String, index=True, nullable=False)        # e.g. "SQ010_SH0010"
    sequence = Column(String, index=True, nullable=True)     # e.g. "SQ010"

    # Frame range
    frame_start = Column(Integer, nullable=True)
    frame_end = Column(Integer, nullable=True)
    fps = Column(Float, nullable=True)