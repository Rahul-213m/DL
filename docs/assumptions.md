# Assumptions

Every assumption I made while auditing and planning. Recorded per working rule 6.
Each entry: **ID · assumption · basis · how to falsify / what changes if wrong.**

Status legend: `ASSUMED` (not yet confirmed) · `CONFIRMED` (verified from code or runtime).

---

## Environment

| ID | Assumption | Basis | Falsified by |
|---|---|---|---|
| A1 | The deployment target is **ROS 2 Jazzy** on Ubuntu 24.04 / Python 3.12, and the perception "brain" should run **inside the same ROS workspace** rather than as a separate service. | `/opt/ros/jazzy` is the only ROS install present. `attendance_robot/README.md:3` says Humble (stale). `rclpy` is unavailable in `.venv` (Python 3.13). | User confirms Humble as the target, **or** prefers a split ROS/service architecture. Would change the packaging plan in P2/P3. |
| A2 | The `.venv` Python 3.13 environment is the **current dev environment** and is not sacred — packages may be relocated into the ROS workspace. | `.venv/bin/python` is 3.11-era pinned stack running fine on 3.13. | User requires 3.13 to stay. Then ROS must run via a systemd unit + HTTP bridge instead. |
| A3 | `insightface 1.0.1` is the pinned version, **not** the `>=0.7.3` floor in `requirements.txt`. | Import probe reported 1.0.1 installed. | Older insightface required for a specific ONNX model. |

## Architecture

| ID | Assumption | Basis | Falsified by |
|---|---|---|---|
| A4 | `face_gallery` remains the **single source of truth** for embeddings; FAISS stays a rebuildable in-memory cache. This design is preserved. | `app/services/gallery.py:88-114` already implements exactly this, with automatic rebuild on FAISS failure. | Requirement for multi-region or offline gallery sync. |
| A5 | **Gallery expansion (no retraining) remains the primary learning mechanism.** Optional background metric learning is permitted but must never sit on the critical path and must be gated by a frozen validation set. | The original project's stated thesis (`project_overview.md:17`), and it is the correct call for avoiding catastrophic forgetting. | Requirement for higher FAR performance than gallery-only can reach. |
| A6 | The existing manual photo-upload path (`POST /session/{id}/capture`) **stays supported** — it is the hardware-free test path and the review/QA tool. | Already used by 11 sessions in the live DB. | Not stated; retaining it is strictly additive. |
| A7 | The ROS `std_msgs`-only interface is **replaced with custom msg/srv/action** definitions rather than kept. | `package.xml:36-39` calls this a deliberate simplification. Custom types are required for the target architecture (metadata, angle+zoom, actions). | Not stated. |
| A8 | Simulation-only ROS nodes (`motor_controller`, `camera_interface`) are **kept as mock implementations** behind the same interface, not deleted. They are the only way to test without hardware. | `colcon test` passes 57 tests against them; they are the CI substitute for real hardware. | Not stated. |

## Data & Storage

| ID | Assumption | Basis | Falsified by |
|---|---|---|---|
| A9 | **PostgreSQL** is the production database; SQLite stays for dev and unit tests. | `docker-compose.yml:2` already provisions Postgres 16. | Single-node deployment where SQLite is genuinely sufficient. Migration path stays valid either way. |
| A10 | The roster is authoritative **in this system**, not in an external SIS. A `classes` + `class_members` model will be introduced. | No external integration exists; `class_id` is currently a free-text string. | An existing SIS/LMS must be the source of truth. Changes the roster sync design in P4/P6. |
| A11 | Existing data in `attendance.db` (4 students, 315 embeddings, 11 sessions) is **development data that may be migrated or discarded**, and is not required to be preserved byte-for-byte. | Students are `R1`–`R4` with placeholder names; sessions have empty `end_time`. Looks like testing. | These are real student records. Then a data-migration script and consent review are mandatory before any schema change. |
| A12 | Face crops and full classroom frames should have a **class-differentiated retention policy**, not one global `RAW_FRAME_RETENTION_DAYS`. | Different data types carry different privacy weight. | A single institutional retention policy already exists. |

## Operations & Deployment

| ID | Assumption | Basis | Falsified by |
|---|---|---|---|
| A13 | The deployment is a **single physical machine** (notebook/NUC/mini-PC) co-located with the robot, unless told otherwise. | Only one machine visible in this environment. | Separate GPU inference host. Changes the split of P3/P4 work. |
| A14 | There may be **no GPU**, and the CPU path must be made genuinely fast enough, with GPU acceleration as an opportunistic accelerator (ONNX Runtime CUDA/TensorRT provider when present). | `.env` sets `INSIGHTFACE_PROVIDERS=CPUExecutionProvider`; `torch` is not installed. | A CUDA GPU is available. Then TensorRT + batching becomes a first-class requirement. |
| A15 | One-command setup via Docker Compose is the target, with ROS launched via systemd units inside the same container or host. | `docker-compose.yml` exists and is minimal. | A systemd-only, no-Docker deployment is mandated. |
| A16 | The scheduled-scan timetable will be provided as **YAML configuration** (timetable of class → time), not via an external calendar API (Google Calendar, etc.). | Not stated; simplest robust option. | External calendar sync required. |

## Security & Privacy

| ID | Assumption | Basis | Falsified by |
|---|---|---|---|
| A17 | The current `API_KEY=changeme-dev-key` and everything committed in `.env` are **treated as compromised** and rotated in P1. | `.env` is git-tracked; the key is a public default string also printed in `HOW_TO_RUN.txt:29`. | — (assumed regardless; rotation is correct either way) |
| A18 | All biometric data already committed to git (`data/` 850 MB, `ENROLL_PHOTOS/` 74 MB) requires an explicit **retention/erasure decision** before the next push, and the history will be rewritten. | Verified: `git ls-files` lists all of it; `.git` is 919 MB. | — (non-negotiable under DPDP/GDCP posture) |
| A19 | Authentication will move from a shared API key to **per-user credentials with roles** (admin / teacher / read-only), using either OIDC or local accounts with hashed passwords. | Target spec requires RBAC. | An institutional SSO provider exists and must be used. Changes P6 auth design only. |
| A20 | Encryption at rest will use **application-level or volume-level encryption** for embeddings and images; TLS terminated at the reverse proxy. | Target spec requires both. | A HSM or KMS is mandated. |

## Model & Licensing

| ID | Assumption | Basis | Falsified by |
|---|---|---|---|
| A21 | Deployment is **institutional/academic** for now, so the non-commercial `buffalo_l` weights are usable. | `README.md:198-200` already flags this. | Commercial deployment intended → propose an AdaFace / alternative-licensed backbone instead. **This is a blocking question (Q5).** |
| A22 | InsightFace **SCRFD 10G** remains the detector (already used, ONNX, fast on CPU), rather than switching to a YOLO-face model. | It is already wired up and is a proven strong choice for small/dense faces. | Benchmark shows SCRFD misses back-row faces at target coverage. |
| A23 | The system will **not** include a face anti-spoof/liveness model in the initial production path, but the interface will be reserved for one. | Current README explicitly states no liveness. | Institution requires spoof resistance → a Silent-Face or similar model becomes mandatory, with its own licensing review. |
| A24 | Anti-spoofing, if later added, will be a **separate ROS node with its own decision**, not folded into the recognizer. | Separation of concerns; keeps the core unit-testable without the model. | — |

## Quality & Testing

| ID | Assumption | Basis | Falsified by |
|---|---|---|---|
| A25 | Existing tests are **preserved and extended**, not replaced. The 23 Python tests encode correct business rules. | They assert semantics (manual > auto, unconfirmed ≠ present, DB survives FAISS failure). | — |
| A26 | The three test suites (`tests/`, `attendance_robot/test/`) will be **unified under one `pytest` invocation** with `rclpy` importable, plus a CI job that does not require hardware. | Currently `pytest` at the repo root **fails collection** because `attendance_robot/test/test_angle_utils.py` imports `rclpy` from a 3.13 venv that lacks it. | — |
| A27 | A **held-out evaluation set** of real classroom images does not yet exist. I will provide a collection protocol and an evaluation script; I will not invent numbers until data exists. | Live DB has 32 attendance events total, 4 students. Nowhere near an evaluation set. | A labelled evaluation set already exists somewhere. Provide the path and I will use it. |
| A28 | Acceptance metrics (TAR@FAR, coverage %, duplicate rate, unknown rate trend, end-to-end scan time) will be reported as **measured**, **UNVERIFIED with a protocol**, or **BLOCKED on data** — never as estimates presented as results. | Working rule 4. | — |

## Out of Scope for Now

| ID | Assumption | Basis |
|---|---|---|
| A29 | LMS integration (Moodle/Google Classroom/Canvas) via webhook is **optional and last** in P6, behind an adapter interface. | Not stated; no LMS named. |
| A30 | Web dashboard will be a **new** Streamlit/React app, not an extension of the 713-line `ui/app.py`. The existing UI is preserved as a working reference but is too monolithic to grow into a conversational operator console. | `ui/app.py` reads and writes `.env` and holds all workflow in one file. |
