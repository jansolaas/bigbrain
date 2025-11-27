from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from app.database import Base


class Sequence(Base):
    __tablename__ = "sequences"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("projects.id"), index=True, nullable=False)
    episode_id = Column(Integer, ForeignKey("episodes.id"), index=True, nullable=True)

    name = Column(String, index=True, nullable=False)      # e.g. "SQ010"
    description = Column(Text, nullable=True)