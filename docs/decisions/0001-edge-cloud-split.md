# ADR 0001 — Split edge (ROS 2 Jazzy / Python 3.12) from cloud (Python 3.13)

- **Status:** Accepted (operator decision, 2026-09-29)
- **Context:** The legacy repo contained two systems in one folder that could not
  talk: ROS 2 nodes needing `rclpy` from Python 3.12, and a FastAPI/InsightFace
  app running in a Python 3.13 virtualenv. `rclpy` is not installable into the
  app venv, so no single interpreter could run both.
- **Decision:** Keep the runtimes separate.
  - **Edge** (`ros_ws/`): ROS 2 Jazzy, Python 3.12, small classroom computer, no
    GPU. Owns camera, servo, scan planning, and an offline-capable uploader.
  - **Cloud** (`app/`): Python 3.13, FastAPI, PostgreSQL, S3, GPU workers.
    Owns perception, identity, attendance and the operator console.
- **Rationale:** One runtime would have been simpler, but the edge needs a
  stable, small, offline-first install while the cloud needs a modern data stack
  and GPU inference. Merging them would drag either a 3 GB ML stack or a
  heavyweight ROS install onto every classroom device, and would make the
  classroom node depend on cloud availability at startup.
- **Consequences:**
  - Interfaces between the two must be explicit and versioned (see ADR 0003).
  - Contracts between them are tested independently of ROS.
  - The edge can complete a scan with the network down; results are queued.
- **Rejected:** single runtime on Python 3.12 (worse GPU/data tooling), single
  runtime on 3.13 (no `rclpy`), microservice-per-node (over-engineering at this
  size).
