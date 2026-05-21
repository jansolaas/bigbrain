from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    discord_id: Optional[str] = None
    full_name: Optional[str] = None
    role: str = "artist"
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    discord_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)