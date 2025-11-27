from sqlalchemy.orm import Session

from app.models import (
    Project,
    Shot,
    Sequence,
    Asset,
    Task,
    TaskType,
    TaskStatus,
    User,
    Version,
    Software,
)


def seed_dev_data(db: Session) -> None:
    """Seed some development data if the DB is empty."""
    # If there are already projects, assume we've seeded before
    existing_project = db.query(Project).first()
    if existing_project:
        return

    # 1. Create a default User
    admin = User(
        username="admin",
        email="admin@bigbrain.com",
        full_name="Pipeline Admin",
        role="admin",
        discord_id="admin#0001"
    )
    # Create a default user
    admin_user = User(
        username="PythonSaurus",
        full_name="jan",
        role="admin",
        email="jan@saurus.no",
        discord_id="987064689928314880")

    supervisor_user = User(
        username="HoudinOsaurus",
        full_name="sondre",
        role="supervisor",
        email="sondre@saurus.no")

    artist_user = User(
        username="whiskeySaurus",
        full_name="herman",
        role="artist",
        email="herman@saurus.no")

    db.add(admin_user)
    db.add(admin)
    db.add(supervisor_user)
    db.add(artist_user)
    db.flush() # Get admin.id

    # SEED SOFTWARE FIRST (so projects can theoretically use them)
    maya_24 = Software(name="maya", version="2024.2", exec_path="/usr/autodesk/maya2024/bin/maya")
    nuke_15 = Software(name="nuke", version="15.0v1", exec_path="/usr/local/Nuke15.0v1/Nuke15.0")
    houdini_19 = Software(name="houdini", version="19.5.640", exec_path="/opt/hfs19.5/bin/houdini")

    db.add(maya_24)
    db.add(nuke_15)
    db.add(houdini_19)
    db.flush()

    # 2. Project 1: Feature film style
    film = Project(
        name="Big Brain Feature",
        code="BBF",
        root_path="/mnt/projects/BBF",
        description="Feature film test project",
        fps=24.0,
        is_active=True,
        config={
            "software": {"maya": "2024.2", "nuke": "15.0v1"},
            "env": {"OCIO": "/mnt/projects/BBF/config.ocio"}
        }
    )
    db.add(film)
    db.flush()

    # 3. Asset for Film
    hero_asset = Asset(
        project_id=film.id,
        name="HeroCharacter",
        type="character",
        project_name=film.name
    )
    db.add(hero_asset)
    db.flush()

    # 4. Version for Asset (v001)
    hero_v1 = Version(
        asset_id=hero_asset.id,
        version_number=1,
        file_path="/mnt/projects/BBF/assets/character/HeroCharacter/v001/hero.ma",
        comment="Initial model publish"
    )
    db.add(hero_v1)

    # 5. Task for Asset (Modeling)
    model_task = Task(
        asset_id=hero_asset.id,
        name="Modeling",
        task_type=TaskType.MODELING,
        status=TaskStatus.IN_PROGRESS,
        assignee_id=admin.id,
        description="Refine facial topology"
    )
    db.add(model_task)

    # 6. Sequence for Film
    film_seq = Sequence(
        project_id=film.id,
        episode_id=None,
        name="SQ010",
        description="Opening sequence",
    )
    db.add(film_seq)
    db.flush()

    # 7. Shots for Film
    film_shot_1 = Shot(
        project_id=film.id,
        sequence_id=film_seq.id,
        name="SQ010_SH0010",
        frame_start=1001,
        frame_end=1100,
        fps=None,  # inherit from project (24)
    )
    db.add(film_shot_1)
    db.flush()

    # 8. Task for Shot (Animation)
    anim_task = Task(
        shot_id=film_shot_1.id,
        name="Animation",
        task_type=TaskType.ANIMATION,
        status=TaskStatus.NOT_STARTED,
        assignee_id=admin.id,
        description="Blocking pass"
    )
    db.add(anim_task)

    # --- Project 2: Episodic style ---
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

    ep1_seq = Sequence(
        project_id=episodic.id,
        episode_id=None,
        name="E01_SQ010",
        description="Episode 1, sequence 10",
    )
    db.add(ep1_seq)
    db.flush()

    ep1_shot_1 = Shot(
        project_id=episodic.id,
        sequence_id=ep1_seq.id,
        name="E01_SQ010_SH0010",
        frame_start=1001,
        frame_end=1050,
        fps=None
    )
    db.add(ep1_shot_1)

    db.commit()