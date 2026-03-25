from pydantic import BaseModel, ConfigDict


class AssetBase(BaseModel):
    project_id: int
    name: str
    type: str


class AssetCreate(AssetBase):
    """Schema for creating an asset (request body)."""
    pass


class AssetOut(AssetBase):
    """Schema for reading an asset (response)."""
    id: int

    # Allow constructing from ORM objects (SQLAlchemy models)
    model_config = ConfigDict(from_attributes=True)