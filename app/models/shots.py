from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class Shot(Base):
    __tablename__ = "shots"

    id = Column(Integer, primary_key=True, index=True)

    # Link to project and sequence (both required now)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True, nullable=False)
    sequence_id = Column(Integer, ForeignKey("sequences.id"), index=True, nullable=False)

    # Simple identifier for the shot
    name = Column(String, index=True, nullable=False)

    # Frame range
    frame_start = Column(Integer, nullable=True)
    frame_end = Column(Integer, nullable=True)

    # Optional fps override
    fps = Column(Float, nullable=True)