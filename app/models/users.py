from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    discord_id = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    role = Column(String, default="artist")  # e.g. "artist", "lead", "admin"
    is_active = Column(Boolean, default=True)