2. **Schemas**:
    - These are **data validation** and **serialization layers**, built using Pydantic.
    - They ensure that any data sent to or from your API is well-structured, consistent, and conforms to business rules.
    - Schemas are purely Python objects, disconnected from the database, and used to handle input/output data for your API endpoints.


#### 2. **Schemas (Pydantic Data Validation & Serialization Layer)**:
Schemas define the **input/output structure** for the Version-related API endpoints. They ensure you're working with clean, validated data and specify what data is returned.
**VersionBase** schema:
``` python
class VersionBase(BaseModel):
    asset_id: int
    file_path: str
    comment: Optional[str] = None
    version_type: VersionType
    department: str
    task: str
```
- **Purpose**: Serves as the base schema for all input/output data. This ensures that any data being used matches this structure.
    - Example: Whenever a client sends a request to create a version, we validate the `asset_id`, `file_path`, `version_type`, and other fields against this schema.

- **Asset_ID**: Since it’s in `VersionBase`, it means every operation involving a "version" (input or output) will expect or use an `asset_id`.

**VersionCreate** schema:
``` python
class VersionCreate(VersionBase):
    """Schema for creating a version."""
    pass
```
- **Purpose**: This schema directly inherits all the fields from `VersionBase`.
    - Even if the class is empty, it’s **important conceptually** because it tells developers and the codebase, "This schema is specifically for creating new versions."
    - Example: All input validation for the `/versions` `POST` endpoint would use this schema.

**VersionOut** schema:
``` python
class VersionOut(VersionBase):
    id: int
    version_number: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```
- **Purpose**: This schema is for **output**—when API clients (e.g., your frontend or tools) request data about versions.
- It includes fields that come from the database (e.g., `id`, `version_number`, and `created_at` are database-derived values, not provided by the client).
- This schema ensures consumers of your API only see relevant data and not sensitive/internal database structures.
