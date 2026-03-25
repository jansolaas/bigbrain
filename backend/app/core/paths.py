import os
from app.models import Project, Sequence, Shot


def ensure_folder(path: str):
    """Safely create a folder if it doesn't exist."""
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f"Created: {path}")
        except OSError as e:
            print(f"Error creating {path}: {e}")

def create_project_structure(project: Project):
    """Create the root project folder."""
    ensure_folder(project.root_path)
    # Create standard project folders if needed (e.g. 'shots', 'assets')
    ensure_folder(os.path.join(project.root_path, "shots"))
    ensure_folder(os.path.join(project.root_path, "assets"))
    ensure_folder(os.path.join(project.root_path, "sequences"))

def create_shot_structure(project: Project, sequence: Sequence, shot: Shot):
    """Create folders for a Shot based on templates."""
    config = project.config or {}
    templates = config.get("templates", {})
    structure = config.get("structure", {})

    # 1. Get the template (defaulting to a hardcoded fallback if missing)
    # Using the seed names: project_root, sequence, shot
    template = templates.get("shot_root", "{project_root}/shots/{sequence}/{shot}")

    # 2. Resolve the path
    # We use python's string format to replace {keys}
    try:
        shot_path = template.format(
            project_root=project.root_path,
            sequence=sequence.name,
            shot=shot.name
        )
    except KeyError as e:
        print(f"Template Error: Missing key {e}")
        return

    # 3. Create the root shot folder
    ensure_folder(shot_path)

    # 4. Create sub-structure
    subfolders = structure.get("shot", [])
    for sub in subfolders:
        full_path = os.path.join(shot_path, sub)
        ensure_folder(full_path)

    return shot_path