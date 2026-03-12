# BigBrain Pipeline

**BigBrain** is an in-house pipeline tool for animation studios, built with **FastAPI** and **SQLAlchemy**. It provides a complete backend API for managing projects, shots, assets, tasks, versions, and user workflows in a production environment.

---

## Features

### Core Data Management
- **Projects**: Organize work with project-level configurations (software versions, environment variables, folder templates).
- **Episodes & Sequences**: Support for episodic and feature workflows.
- **Shots**: Frame-accurate shot tracking with fps inheritance.
- **Assets**: Character, prop, environment, and FX asset management.
- **Versions**: Immutable publish tracking with auto-incrementing version numbers.
- **Tasks**: Assignment and status tracking (modeling, rigging, animation, lighting, compositing, etc.).

### Pipeline Features
- **Software Registry**: Centralized DCC version management (Maya, Nuke, Houdini).
- **Folder Creation**: Automatic directory structure generation based on project templates.
- **FPS Inheritance**: Project → Shot fps override system.
- **Soft Deletes**: `is_active` flags for omitting entities without losing data.
- **User Management**: Role-based users (artist, lead, admin).

### Security
- **JWT Authentication**: OAuth2 password flow with token-based auth.
- **Role-Based Access Control**: Protect endpoints by role (e.g., only admins can create projects).

### API
- **RESTful Design**: Standard GET/POST/PATCH operations.
- **Auto-Generated Docs**: Swagger UI at `/docs`.
- **Validation**: Pydantic schemas ensure data consistency.

---

## Tech Stack

- **Backend**: FastAPI (async, high-performance)
- **Database**: SQLite (dev) / PostgreSQL (production)
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (python-jose) + bcrypt (passlib)
- **Validation**: Pydantic v2
- **Server**: Uvicorn

---

## Project Structure

---

## Getting Started

### Prerequisites
- **Python 3.9+**
- **pip** and **virtualenv**

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd bigbrain
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - **Windows (cmd):**
     ```bash
     venv\Scripts\activate
     ```
   - **Windows (PowerShell):**
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a `.env` file** (optional, defaults to SQLite):
   ```bash
   DATABASE_URL=sqlite:///./bigbrain.db
   ```

6. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Open the API documentation:**
   Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Quick Start (Seeded Data)

On first run, the system automatically seeds test data:
- **Users**: `admin` (password: `admin123`), `PythonSaurus`, `HoudinOsaurus`, `whiskeySaurus`
- **Projects**: `Big Brain Feature` (BBF), `Big Brain Series` (BBS)
- **Software**: Maya 2024.2, Nuke 15.0v1, Houdini 19.5.640
- **Assets, Shots, Tasks, Versions**: Sample data for testing

### Authentication

1. In the Swagger UI (`/docs`), click the **Authorize** button (top right).
2. Login with:
   - **Username**: `admin`
   - **Password**: `admin123`
3. You can now create projects and perform admin actions.

---

## API Endpoints

| Endpoint                  | Method | Description                        | Auth Required |
|---------------------------|--------|------------------------------------|---------------|
| `/api/v1/auth/login`      | POST   | Login and get JWT token            | No            |
| `/api/v1/projects/`       | GET    | List all projects                  | Yes           |
| `/api/v1/projects/`       | POST   | Create a new project               | Admin only    |
| `/api/v1/sequences/`      | GET    | List sequences                     | Yes           |
| `/api/v1/shots/`          | GET    | List shots                         | Yes           |
| `/api/v1/shots/`          | POST   | Create shot (auto-creates folders) | Yes           |
| `/api/v1/shots/{id}`      | PATCH  | Update shot (e.g., omit)           | Yes           |
| `/api/v1/shots/{id}/fps`  | GET    | Get effective fps for shot         | Yes           |
| `/api/v1/assets/`         | GET    | List assets                        | Yes           |
| `/api/v1/versions/`       | GET    | List versions for an asset         | Yes           |
| `/api/v1/versions/`       | POST   | Publish a new version              | Yes           |
| `/api/v1/tasks/`          | GET    | List tasks                         | Yes           |
| `/api/v1/users/`          | GET    | List users                         | Yes           |
| `/api/v1/software/`       | GET    | List registered DCC software       | Yes           |

Full interactive documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Configuration

### Project Config (Example)

Each project can define software versions, environment variables, and folder structures:

json { "software": { "maya": "2024.2", "nuke": "15.0v1" }, "env": { "OCIO": "/mnt/projects/BBF/config.ocio", "JOB": "/mnt/projects/BBF" }, "templates": { "shot_root": "{project_root}/shots/{sequence}/{shot}", "asset_root": "{project_root}/assets/{type}/{asset}" }, "structure": { "shot": ["work/maya", "work/nuke", "publish/caches", "plates"], "asset": ["work/maya", "publish/model", "publish/rig"] } }``` 

---

## Development

### Reset Database
```
bash
# Windows
del bigbrain.db
# macOS/Linux
rm bigbrain.db
# Then restart the server
uvicorn app.main:app --reload



### Add a New Model
1. Create `app/models/yourmodel.py`
2. Define SQLAlchemy model
3. Export in `app/models/__init__.py`
4. Create matching Pydantic schemas in `app/schemas/yourmodel.py`
5. Create API routes in `app/api/v1/yourmodel.py`
6. Register router in `app/api/v1/__init__.py`

---

## Roadmap

### Next Steps
- [ ] Web-based admin panel (React/Vue)
- [ ] Desktop launcher for DCCs (Qt/PySide6)
- [ ] Episode API endpoints
- [ ] Alembic migrations (for production DB changes)
- [ ] Asset dependency tracking
- [ ] Render job integration (Deadline/Tractor)
- [ ] Review/approval workflow
- [ ] File-based publish validation (checksums, thumbnails)

---

## Contributing

This is just a personal project, so contributions are welcome!

---

## License

MIT License

Copyright (c) 2026 Jan Solås

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.