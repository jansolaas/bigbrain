from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from app.database import Base


class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("projects.id"), index=True, nullable=False)

    name = Column(String, index=True, nullable=False)      # e.g. "EP01"
    code = Column(String, index=True, nullable=True)       # optional additional code
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, index=True)