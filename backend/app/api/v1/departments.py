from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Department, Task, Asset, Shot, User
from app.schemas.department import DepartmentOut, DepartmentCreate

router = APIRouter(prefix="/departments", tags=["departments"])

@router.get("/", response_model=List[DepartmentOut])
def list_departments(
    asset_id: Optional[int] = None,
    shot_id: Optional[int] = None,
    assignee_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Department)
    if asset_id:
        query = query.filter(Department.asset_id == asset_id)
    if shot_id:
        query = query.filter(Department.shot_id == shot_id)
    if assignee_id:
        query = query.filter(Department.assignee_id == assignee_id)
    return query.all()

@router.post("/", response_model=DepartmentOut)
def create_department(payload: DepartmentCreate, db: Session = Depends(get_db)):
    # Validate: must attach to EITHER asset OR shot (not both, not neither)
    if payload.asset_id and payload.shot_id:
        raise HTTPException(status_code=400, detail="Cannot link task to both Asset and Shot")
    if not payload.asset_id and not payload.shot_id:
        raise HTTPException(status_code=400, detail="Must link task to either Asset or Shot")

    # Check foreign keys
    if payload.asset_id:
        if not db.query(Asset).filter(Asset.id == payload.asset_id).first():
            raise HTTPException(status_code=404, detail="Asset not found")
    if payload.shot_id:
        if not db.query(Shot).filter(Shot.id == payload.shot_id).first():
            raise HTTPException(status_code=404, detail="Shot not found")
    if payload.assignee_id:
        if not db.query(User).filter(User.id == payload.assignee_id).first():
            raise HTTPException(status_code=404, detail="User not found")

    department = Department(**payload.model_dump())
    db.add(department)
    db.commit()
    db.refresh(department)
    return department