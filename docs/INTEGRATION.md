# Integration Guide

This is the verified local integration workflow for the attendance system. It is intentionally written from a fresh-clone perspective and reflects the startup paths that were checked in this workspace.

## 1. What is included

The system is split into three runtime pieces:

- Cloud API: FastAPI app served from the repository root.
- Operator UI: Streamlit app served on a separate port.
- Edge ROS stack: simulated or hardware launch for the camera / planner / uploader nodes.

The checked working sequence is:

1. install Python dependencies
2. configure `.env`
3. run DB migrations / schema check
4. start the API
5. start the operator UI
6. start the ROS simulated edge stack
7. validate the expected ports and responses

## 2. Prerequisites

- Python 3.13 is used by the project environment in this workspace.
- ROS 2 is required only for the edge stack. The ROS build script in `ros_ws/build.sh` is the supported path for this environment.
- A local `.env` file is required for startup. Do not commit it.

## 3. Fresh-clone setup

From the repo root:

```bash
cd /path/to/DL_PROJECT
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/generate_secrets.py >> .env
```

Review `.env` and set any required values before continuing. In particular:

- `ENVIRONMENT=development` for local runs
- `API_KEY` and `JWT_SECRET` should be non-empty
- `DATABASE_URL` should be the intended local database
- `MODEL_REGISTRY_CONFIG` can remain empty unless you have a licensed override

Then run the database migration and a config check:

```bash
. .venv/bin/activate
alembic upgrade head
python -m app.cli check_config
python -m app.cli doctor
```

The doctor command is the quickest single validation step. If it fails, fix the configuration before starting services.

## 4. Start the cloud API

```bash
cd /path/to/DL_PROJECT
. .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

A successful startup prints `Uvicorn running on http://127.0.0.1:8000` and then the app is listening.

Validate the service with:

```bash
curl -sS -o /dev/null -w '%{http_code}\n' -X GET http://127.0.0.1:8000/docs
```

Expected result: `200`.

> If port `8000` is already in use, stop the stale listener before retrying:
>
> ```bash
> lsof -i :8000 -t | xargs -r kill -9
> ```

## 5. Start the operator UI

Start a second terminal:

```bash
cd /path/to/DL_PROJECT
. .venv/bin/activate
streamlit run ui/app.py --server.address 127.0.0.1 --server.port 8501 --server.headless true
```

Validate the UI with:

```bash
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8501
```

Expected result: `200`.

> If port `8501` is already in use, clear the stale listener first:
>
> ```bash
> lsof -i :8501 -t | xargs -r kill -9
> ```

## 6. Start the ROS edge stack in simulated mode

This is the validated edge integration path for local testing without hardware:

```bash
cd /path/to/DL_PROJECT/ros_ws
./build.sh
. install/setup.bash
ros2 launch attendance_bringup edge.launch.py mode:=simulated
```

Expected behavior:

- the launch file starts `servo_controller`, `camera_bridge`, `scan_planner`, and `edge_uploader`
- the simulated mode prints `SIMULATED MODE -- no hardware is touched`
- the nodes remain up and do not crash during the simulated run
- the outbox writes captures to the configured temporary location and the uploader tries to send them to the cloud service

The launch script is intentionally safe in simulation and does not require real hardware or a camera bus.

## 7. End-to-end smoke check

The repository includes a local smoke check to verify the product wiring without manual browser use:

```bash
cd /path/to/DL_PROJECT
python scripts/integration_smoke.py
```

This smoke script validates:

- the configuration and licensing checks
- the API returning `200` on the docs endpoint
- the UI returning `200` on the Streamlit port
- the service health path for the integrated environment

## 8. Common issues seen in this environment

### Port conflict

A stale `uvicorn` or `streamlit` process can leave the port bound. The remedy is:

```bash
lsof -i :8000 -t | xargs -r kill -9
lsof -i :8501 -t | xargs -r kill -9
```

### Schema drift

If the app refuses to start because the database schema is behind the code, run:

```bash
alembic upgrade head
```

### ROS Python mismatch

When the ROS build does not behave as expected because the wrong Python is being used, rebuild with the supported script:

```bash
cd ros_ws
./build.sh
```

This script is the verified path for this Linux environment.

## 9. Hard truths before production

The repo is integration-ready for local verification, but some production requirements remain intentionally outside the automated local path:

- real hardware validation is still a separate deployment task
- liveness anti-spoof model support is disabled by design until a licensed model is approved
- production deployment still requires a customer-approved model licensing review and the operating policies called out in `docs/HUMAN_ACTIONS.md`

This integration guide is therefore honest about what has been verified locally and what still requires human/legal sign-off.
