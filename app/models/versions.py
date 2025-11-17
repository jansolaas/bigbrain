from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Version(Base):
    __tablename__ = "versions"

    id = Column(Integer, primary_key=True, index=True)

    # Link to assets table
    asset_id = Column(Integer, ForeignKey("assets.id"), index=True, nullable=False)

    version_number = Column(Integer, nullable=False)

    file_path = Column(String, nullable=False)   # path to the published file on disk/storage
    comment = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())