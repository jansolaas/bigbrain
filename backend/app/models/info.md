1. **Models**:
    - These define the **database structure** and are linked to your actual database (in this case, SQLite or PostgreSQL) through an ORM (Object-Relational Mapper) like SQLAlchemy.
    - Think of these as the "source of truth" for what tables and fields exist in your database.
    - They are used for tasks like querying, creating, updating, and deleting data in the database.


#### 1. **Model (Database Layer)**:
The `Version` model would typically be defined in your `app.models.versions` file. This is an SQLAlchemy class that represents the `versions` table in your database. For example:
``` python
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Version(Base):
    __tablename__ = "versions"

    id = Column(Integer, primary_key=True, index=True)
    version_number = Column(Integer, nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)  # asset FK
    file_path = Column(String, nullable=False)
    comment = Column(String, nullable=True)
    version_type = Column(Enum(VersionType), nullable=False)
    department = Column(String, nullable=False)
    task = Column(String, nullable=False)

    asset = relationship("Asset", back_populates="versions")  # Optional, for ORM relations
```
- **Purpose**: SQLAlchemy generates database commands like `CREATE TABLE`, `INSERT`, and `SELECT` behind the scenes using this model.
- **Relationships**:
    - The `asset_id` is a foreign key. It establishes a relationship to the `Asset` model/table. In the database, we want to associate every `Version` record with an asset.
    - Relationships (like `asset = relationship(...)`) aren't mandatory for basic functionality but can be helpful in complex queries.
