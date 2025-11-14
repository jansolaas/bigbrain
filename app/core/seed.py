from sqlalchemy.orm import Session

from app.models import Project, Shot


def seed_dev_data(db: Session) -> None:
    """Seed some development data if the DB is empty."""
    # If there are already projects, assume we've seeded before
    existing_project = db.query(Project).first()
    if existing_project:
        return

    # Project 1: Feature film style
    film = Project(
        name="Big Brain Feature",
        code="BBF",
        root_path="/mnt/projects/BBF",
        description="Feature film test project",
        fps=24.0,
        is_active=True,
    )
    db.add(film)
    db.flush()  # get film.id without committing yet

    # A couple of shots for film
    film_shot_1 = Shot(
        project_id=film.id,
        name="SQ010_SH0010",
        sequence="SQ010",
        frame_start=1001,
        frame_end=1100,
        fps=None,  # inherit from project (24)
    )
    film_shot_2 = Shot(
        project_id=film.id,
        name="SQ010_SH0020",
        sequence="SQ010",
        frame_start=1101,
        frame_end=1200,
        fps=12.0,  # override
    )
    db.add(film_shot_1)
    db.add(film_shot_2)

    # Project 2: Episodic style
    episodic = Project(
        name="Big Brain Series",
        code="BBS",
        root_path="/mnt/projects/BBS",
        description="Episodic test project",
        fps=25.0,
        is_active=True,
    )
    db.add(episodic)
    db.flush()

    # Shots could encode episode/sequence in name for now (until we add real Episode/Sequence tables)
    ep1_shot_1 = Shot(
        project_id=episodic.id,
        name="E01_SQ010_SH0010",
        sequence="E01_SQ010",
        frame_start=1001,
        frame_end=1050,
        fps=None,  # inherit 25
    )
    db.add(ep1_shot_1)

    db.commit()