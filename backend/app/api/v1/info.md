3. **API (Router & Endpoints)**:
    - This is what users or systems interact with. APIs expose functionality, validate incoming data using schemas, and then perform database operations using models.
    - Think of APIs as the "bridge" between external input (e.g., an HTTP request) and internal logic (working with models and databases).

#### 3. **API (Endpoint)**:
The API ties everything together by:
- Accepting input (validated against the `VersionCreate` schema),
- Performing business logic and querying the database (using the `Version` model),
- Returning output validated by the `VersionOut` schema.

For example:
``` python
@router.post("/", response_model=VersionOut, status_code=201)
def create_version(payload: VersionCreate, db: Session = Depends(get_db)):
    """Create a new version for an asset (minimal publish record)."""

    # Ensure asset exists
    asset = db.query(Asset).filter(Asset.id == payload.asset_id).first()
    if asset is None:
        raise HTTPException(status_code=400, detail="Asset does not exist")

    # Determine the next available version number
    latest = (
        db.query(Version)
        .filter(Version.asset_id == payload.asset_id)
        .order_by(Version.version_number.desc())
        .first()
    )
    next_version = (latest.version_number + 1) if latest else 1

    # Create and save the version
    version = Version(
        asset_id=payload.asset_id,
        file_path=payload.file_path,
        comment=payload.comment,
        version_type=payload.version_type,
        department=payload.department,
        task=payload.task,
        version_number=next_version,
    )

    db.add(version)
    db.commit()
    db.refresh(version)

    return version
```
- **Input**: The `payload` is parsed/validated using the `VersionCreate` schema.
- **Database Query**: SQLAlchemy is used to:
    1. Ensure the referenced asset exists (`Asset.id == payload.asset_id`).
    2. Retrieve the latest version for the given asset to calculate `next_version`.
    3. Insert the new `Version` into the database.

- **Output**: The `Version` is serialized to the `VersionOut` schema before being returned to the client.
