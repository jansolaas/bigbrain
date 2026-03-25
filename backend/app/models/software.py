from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Software(Base):
    __tablename__ = "software"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)  # e.g. "maya"
    version = Column(String, index=True, nullable=False)  # e.g. "2024.2"
    # Path to executable (optional but useful for the launcher)
    exec_path = Column(String, nullable=True)

    # Is this version valid for new projects?
    is_active = Column(Boolean, default=True)