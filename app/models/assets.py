from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)

    # Link to projects table
    project_id = Column(Integer, ForeignKey("projects.id"), index=True, nullable=False)

    # Optional: keep project_name for now (can be removed later)
    project_name = Column(String, index=True)

    name = Column(String, unique=True, index=True)
    type = Column(String, index=True)