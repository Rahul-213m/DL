# System Runbook

This document explains how to run the full classroom attendance system, what must be configured before startup, and which components are required for the cloud API and the ROS edge stack.

## 1. System overview

The project has two main parts:

1. Cloud service
   - FastAPI application in `app/`
   - Runs on port `8000`
   - Handles enrollment, attendance processing, API routes, and database access

2. ROS edge system
   - Workspace in `ros_ws/`
   - Runs on the ROS 2 Jazzy stack
   - Starts the camera node, planner, servo controller, and uploader
   - Simulated mode is the safest way to validate the full edge flow without hardware

The normal developer flow is:
- start the cloud API
- build and source the ROS workspace
- launch the simulated or hardware edge stack
- use the Streamlit UI for operator interaction

---

## 2. Prerequisites

### Python environment

The repo expects a Python virtual environment in the project root:

```bash
cd ~/Documents/DL_PROJECT
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The project is validated against the pinned dependency set in `pyproject.toml`.

### ROS 2 environment

ROS 2 Jazzy is expected to be installed on the machine.

Check:

```bash
source /opt/ros/jazzy/setup.bash
ros2 --version
```

If ROS is not installed, install the Jazzy desktop or base distribution for your OS first.

### System dependencies

Make sure these are available:
- Python 3.11+
- `colcon`
- `rosdep` if needed by your ROS install
- `sqlite3` for database inspection
- `curl` for quick API checks
- `lsof` or `ss` for port checking

---

## 3. Required configuration before startup

### 3.1 Database

The app expects the SQLite database file to be present and schema-updated.

From the project root:

```bash
cd ~/Documents/DL_PROJECT
source .venv/bin/activate
alembic upgrade head
```

This brings the database to the expected migration revision.

If the schema is stale, the app will fail at startup with a missing-table error.

### 3.2 API environment

The project uses environment settings from the app config. The app will run in development mode by default unless explicitly configured otherwise.

Typical dev values:
- `ENVIRONMENT=development`
- `API_KEY=changeme-dev-key`
- model backends set to the permissive baseline unless a commercial override is supplied

If you use custom configuration, make sure the `.env` file is present and valid before starting the server.

### 3.3 Model setup

The app loads model backends through the registry. In dev mode the startup path is allowed to use the permissive baseline:
- detector: `opencv_yunet`
- embedder: `opencv_sface`

Commercial deployment requires a legal review of the model licensing posture as documented in:
- `docs/model_licensing.md`
- `docs/HUMAN_ACTIONS.md`

Do not deploy a non-commercial model in production without a proper commercial licence record.

---

## 4. Start the cloud service

Open a terminal and run:

```bash
cd ~/Documents/DL_PROJECT
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The API should be available at:
- http://127.0.0.1:8000
- Swagger docs: http://127.0.0.1:8000/docs

### If port 8000 is already in use

Check the process:

```bash
lsof -i :8000
```

Then stop the stale process:

```bash
kill <PID>
```

Then restart the API.

---

## 5. Start the Streamlit UI

In a second terminal:

```bash
cd ~/Documents/DL_PROJECT
source .venv/bin/activate
streamlit run ui/app.py --server.address 127.0.0.1 --server.port 8501
```

Open:
- http://127.0.0.1:8501

This is the operator UI used to interact with the attendance workflow.

---

## 6. Build the ROS workspace

From the ROS workspace directory:

```bash
cd ~/Documents/DL_PROJECT/ros_ws
./build.sh
```

This script intentionally strips conda-derived Python entries from `PATH` and forces ROS to use the system Python at `/usr/bin/python3`, which is required for Jazzy compatibility.

If the script fails, check that:
- ROS Jazzy is sourced
- `/usr/bin/python3` exists
- no conda environment is shadowing the ROS build

---

## 7. Source the ROS workspace

After the build completes:

```bash
cd ~/Documents/DL_PROJECT/ros_ws
source install/setup.bash
```

This exposes the ROS nodes and interfaces to the shell.

---

## 8. Run the ROS edge system

### Simulated mode

This is the safest default for validation and local testing:

```bash
ros2 launch attendance_bringup edge.launch.py mode:=simulated
```

This starts the full edge stack without touching hardware:
- camera bridge
- scan planner
- servo controller
- uploader

### Hardware mode

For real classroom hardware:

```bash
ros2 launch attendance_bringup edge.launch.py mode:=hardware
```

This is the real deployment path and should only be used after hardware commissioning and safety review.

---

## 9. Recommended full startup order

For a normal local full-system check, use this order:

### Terminal 1
```bash
cd ~/Documents/DL_PROJECT
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 2
```bash
cd ~/Documents/DL_PROJECT
source .venv/bin/activate
streamlit run ui/app.py --server.address 127.0.0.1 --server.port 8501
```

### Terminal 3
```bash
cd ~/Documents/DL_PROJECT/ros_ws
./build.sh
source install/setup.bash
ros2 launch attendance_bringup edge.launch.py mode:=simulated
```

---

## 10. Useful validation commands

### API health

```bash
curl http://127.0.0.1:8000/docs
```

### UI availability

Open in browser:
- http://127.0.0.1:8501

### ROS workspace health

```bash
cd ~/Documents/DL_PROJECT/ros_ws
source install/setup.bash
ros2 topic list
```

### Run ROS tests

```bash
cd ~/Documents/DL_PROJECT/ros_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
colcon test
```

---

## 11. Deployment and operational caution

Before production deployment:
- confirm model licensing and provenance
- review data consent and retention requirements
- verify the database schema is current
- test the simulated edge flow before hardware use
- keep the API, UI, and ROS launch processes separate and clearly scoped

The repo includes explicit compliance and legal guidance in:
- `docs/model_licensing.md`
- `docs/HUMAN_ACTIONS.md`

---

## 12. Quick start summary

```bash
cd ~/Documents/DL_PROJECT
source .venv/bin/activate
alembic upgrade head
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Second terminal:

```bash
cd ~/Documents/DL_PROJECT
source .venv/bin/activate
streamlit run ui/app.py --server.address 127.0.0.1 --server.port 8501
```

Third terminal:

```bash
cd ~/Documents/DL_PROJECT/ros_ws
./build.sh
source install/setup.bash
ros2 launch attendance_bringup edge.launch.py mode:=simulated
```
