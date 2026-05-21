from sqlalchemy.orm import Session
from app.core.security import get_password_hash
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
        hashed_password=get_password_hash("adminsaurus"),
        discord_id="admin#0001"
    )
    # Create a default user
    admin_user = User(
        username="PythonSaurus",
        full_name="jan",
        role="admin",
        hashed_password=get_password_hash("autosaurus"),
        email="jan@saurus.no",
        discord_id="987064689928314880")

    supervisor_user = User(
        username="HoudinOsaurus",
        full_name="sondre",
        role="supervisor",
        hashed_password=get_password_hash("sondresaurus"),
        email="sondre@saurus.no")

    artist_user = User(
        username="whiskeySaurus",
        full_name="herman",
        role="artist",
        hashed_password=get_password_hash("herminator"),
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
    # 2. Helper functions for project seed data
    def create_assets_for_project(project: Project, asset_specs: list[tuple[str, str]]) -> list[Asset]:
        assets = []

        for asset_name, asset_type in asset_specs:
            asset = Asset(
                project_id=project.id,
                name=asset_name,
                type=asset_type,
                project_name=project.name,
            )
            db.add(asset)
            assets.append(asset)

        db.flush()
        return assets

    def create_sequences_and_shots(
        project: Project,
        sequence_names: list[str],
        shots_per_sequence: int = 4,
        shot_duration: int = 100,
    ) -> list[Shot]:
        shots = []

        for sequence_name in sequence_names:
            sequence = Sequence(
                project_id=project.id,
                episode_id=None,
                name=sequence_name,
                description=f"{sequence_name} sequence for {project.name}",
            )
            db.add(sequence)
            db.flush()

            for shot_index in range(1, shots_per_sequence + 1):
                shot_number = shot_index * 10
                frame_start = 1001
                frame_end = frame_start + shot_duration - 1

                shot = Shot(
                    project_id=project.id,
                    sequence_id=sequence.id,
                    name=f"{sequence_name}_SH{shot_number:04d}",
                    frame_start=frame_start,
                    frame_end=frame_end,
                    fps=None,
                )
                db.add(shot)
                shots.append(shot)

        db.flush()
        return shots

    # 3. Project 1: Feature film style
    film = Project(
        name="Big Brain Feature",
        code="BBF",
        root_path="C:/BigBrain/projects/BBF",
        description="Feature film test project",
        fps=24.0,
        is_active=True,
        config={
            "software": {"maya": "2024.2", "nuke": "15.0v1"},
            "env": {"OCIO": "/mnt/projects/BBF/config.ocio"},
            "templates": {
                "sequence_root": "{project_root}/sequences/{sequence}",
                "shot_root": "{project_root}/shots/{sequence}/{shot}",
                "asset_root": "{project_root}/assets/{type}/{asset}",
            },
            "structure": {
                "shot": ["work/maya", "work/nuke", "publish/caches", "publish/renders", "plates"],
                "asset": ["work/maya", "work/zbrush", "publish/model", "publish/rig"],
            },
        },
    )
    db.add(film)
    db.flush()

    film_assets = create_assets_for_project(
        film,
        [
            ("Righeous", "character"),
            ("Evol", "character"),
            ("CaptainMorrow", "character"),
            ("DriftBike", "vehicle"),
            ("SignalTower", "environment"),
            ("AncientGate", "prop"),
            ("ForestOutpost", "environment"),
            ("EnergyCore", "prop"),
        ],
    )

    film_shots = create_sequences_and_shots(
        film,
        sequence_names=["SQ010", "SQ020", "SQ030"],
        shots_per_sequence=4,
        shot_duration=100,
    )

    # 4. Version for first Film asset
    hero_v1 = Version(
        asset_id=film_assets[0].id,
        version_number=1,
        file_path="/mnt/projects/BBF/assets/character/Righeous/v001/righeous.ma",
        comment="Initial model publish",
    )
    db.add(hero_v1)

    # 5. Task for first Film asset
    model_task = Task(
        asset_id=film_assets[0].id,
        name="Modeling",
        task_type=TaskType.MODELING,
        status=TaskStatus.IN_PROGRESS,
        assignee_id=admin.id,
        description="Refine facial topology",
    )
    db.add(model_task)

    # 6. Task for first Film shot
    anim_task = Task(
        shot_id=film_shots[0].id,
        name="Animation",
        task_type=TaskType.ANIMATION,
        status=TaskStatus.NOT_STARTED,
        assignee_id=admin.id,
        description="Blocking pass",
    )
    db.add(anim_task)

    # 7. Project 2: Animation project
    saboteur = Project(
        name="Saboteur",
        code="SAB",
        root_path="C:/BigBrain/projects/SAB",
        description="Stylized animation project",
        fps=24.0,
        is_active=True,
        config={
            "software": {"maya": "2024.2", "houdini": "19.5.640", "nuke": "15.0v1"},
            "env": {"OCIO": "/mnt/projects/SAB/config.ocio"},
            "templates": {
                "sequence_root": "{project_root}/sequences/{sequence}",
                "shot_root": "{project_root}/shots/{sequence}/{shot}",
                "asset_root": "{project_root}/assets/{type}/{asset}",
            },
            "structure": {
                "shot": ["work/layout", "work/animation", "work/lighting", "publish/renders", "plates"],
                "asset": ["work/model", "work/rig", "work/surfacing", "publish/model", "publish/rig"],
            },
        },
    )
    db.add(saboteur)
    db.flush()

    saboteur_assets = create_assets_for_project(
        saboteur,
        [
            ("Saboteur", "character"),
            ("CommanderVale", "character"),
            ("CourierBot", "character"),
            ("RailSpeeder", "vehicle"),
            ("CheckpointGate", "environment"),
            ("ClockworkBomb", "prop"),
            ("CityRooftops", "environment"),
            ("ControlRoom", "environment"),
        ],
    )

    saboteur_shots = create_sequences_and_shots(
        saboteur,
        sequence_names=["SQ010", "SQ020", "SQ030"],
        shots_per_sequence=4,
        shot_duration=100,
    )

    # 8. Version for first Saboteur asset
    saboteur_v1 = Version(
        asset_id=saboteur_assets[0].id,
        version_number=1,
        file_path="/mnt/projects/SAB/assets/character/Saboteur/v001/saboteur.ma",
        comment="Initial character model publish",
    )
    db.add(saboteur_v1)

    # 9. Task for first Saboteur asset
    saboteur_model_task = Task(
        asset_id=saboteur_assets[0].id,
        name="Modeling",
        task_type=TaskType.MODELING,
        status=TaskStatus.NOT_STARTED,
        assignee_id=admin.id,
        description="Create primary character model",
    )
    db.add(saboteur_model_task)

    # 10. Task for first Saboteur shot
    saboteur_anim_task = Task(
        shot_id=saboteur_shots[0].id,
        name="Animation",
        task_type=TaskType.ANIMATION,
        status=TaskStatus.NOT_STARTED,
        assignee_id=admin.id,
        description="Initial animation blocking",
    )
    db.add(saboteur_anim_task)

    db.commit()