from sqlalchemy.orm import Session

from app.models import Shot, Project


def resolve_fps_for_shot(db: Session, shot_id: int) -> float:
    """
    Resolve the effective fps for a shot.
    Priority:
      1) shot.fps (if not None)
      2) project.fps (if not None)
    Raises ValueError if no fps is defined anywhere.
    """
    shot = db.query(Shot).filter(Shot.id == shot_id).first()
    if shot is None:
        raise ValueError(f"Shot with id={shot_id} does not exist")

    if shot.fps is not None:
        return shot.fps

    project = db.query(Project).filter(Project.id == shot.project_id).first()
    if project and project.fps is not None:
        return project.fps

    raise ValueError(f"No fps defined for shot id={shot_id} or its project")