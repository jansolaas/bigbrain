from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Task, Asset, Shot, User
from app.schemas.task import TaskOut, TaskCreate

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskOut])
def list_tasks(
    asset_id: Optional[int] = None,
    shot_id: Optional[int] = None,
    assignee_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Task)
    if asset_id:
        query = query.filter(Task.asset_id == asset_id)
    if shot_id:
        query = query.filter(Task.shot_id == shot_id)
    if assignee_id:
        query = query.filter(Task.assignee_id == assignee_id)
    return query.all()

@router.post("/", response_model=TaskOut)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
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

    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task