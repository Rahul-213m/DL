# Archive

Code that was **removed from the active tree** and why. Nothing here is
referenced by the running service. It is kept because deleting your work is
destructive and because the reasoning behind a removed design is sometimes the
most valuable thing in the repository.

The files are still in git history at the commits that last touched them, so
this directory is a convenience, not the only copy.

---

## `legacy/` — pre-W3 capture pipeline

**Moved:** 2026-09-29, W3.

**Why.** `app/api/routes.py` had reached 597 lines mixing HTTP parsing,
business rules, SQLAlchemy queries and FAISS calls. Business rules could only
be tested through a `TestClient` with a live database, and the detection path
lacked the channel-order, orientation, quality-gate and margin fixes that W2
introduced.

**What replaced it, and where the behaviour went.**

| Legacy behaviour | Now lives in | Notes |
|---|---|---|
| `Image.open(...).convert("RGB")` into InsightFace | `app/core/domain/imageops.decode` | **Bug fixed.** Was RGB into a BGR-only graph. Measured +0.079 separability. |
| `_is_duplicate` — one query per detected face | `app/core/domain/dedup` + a per-frame cache in `app/services/attendance.py` | **Fixed.** Was O(F×P) with a DB round trip per face. |
| `gallery_index.search()` returning k=1 raw vectors | `app/services/vector_index.VectorIndex` | **Changed.** Now one result per identity, with gallery depth reported. |
| `route_match` argmax on a single threshold | `app/core/domain/decision.decide` | **Changed.** Score + margin + roster prior. |
| `_detect_faces` tiling | `app/core/domain/geometry.plan_tiles` + `app/pipeline/perception.py` | **Fixed.** Full-frame pass now counted against the tile cap. |
| No quality gate at all | `app/core/domain/quality.assess` | **New.** Three tiers; a poor face can never auto-confirm. |
| Evidence = raw bounding-box slice | `app/core/domain/geometry.aligned_crop` | **Fixed.** Evidence is now the warp the embedder consumed. |
| `absentees()` against every enrolled student | `app/core/domain/attendance.classify` | **Changed.** Per-class roster, plus an UNVERIFIED state. |
| No session close-out | `app/core/domain/session.Session` | **New.** Idempotent close with a recorded reason. |
| `BackgroundTasks` (40-thread AnyIO pool) | `app/core/domain/jobs.WorkerPool` | **Changed.** Explicit concurrency bound, idempotent, retrying. |
| `scripts/purge_old_frames.py` (2 image classes) | `app/retention.py` | **Changed.** All four classes, dry-run by default. |

**What was deliberately kept in the active tree**, because it is right:

- `app/models/schema.py` — the ORM tables. Still the schema.
- `app/services/gallery.py` — `face_gallery` as source of truth with the
  index as a rebuildable cache. This was the best architectural decision in the
  original code and it survives intact.
- `CONFIRMED_MATCH_TYPES` and the `present` / `pending` / `absent` query
  contract. Unconfirmed must never be reported as present; that discipline is
  correct and is now tested.
- Review `resolve` / `dismiss` / `reopen`, including `reopen` removing the
  gallery entry that `resolve` added. Fully reversible human decisions.

**Tests that were kept, not rewritten.** All 23 original behavioural tests
still pass, including the ones that pin those decisions. Two call sites were
mechanically updated because the index API changed shape
(`gallery_index.entries = []` → `gallery_index.reset()`, and unpacking a
`(roll_no, score)` tuple → `.best.roll_no`). Every behavioural assertion is
untouched; only the mechanism changed. That is called out in the W3 commit.

---

## `ROS_ARCHIVE.md` — the original `attendance_robot/` package

**Moved:** 2026-09-29, W5, to `ros_ws/src/attendance_mocks/`.

**Why.** Reconciliation finding: `~/ros_ws` **does not exist**, and
`~/ros2_ws` is an unrelated ROS 2 tutorial workspace (`cpp_pubsub`,
`turtle_shapes`, `urdf_tutorial`, `cpp_srvcli`). `attendance_robot/` was the
**only** copy of the attendance ROS code, so there was nothing to merge — it
became the canonical workspace content.

**What was preserved.** The nodes were good for what they simulated, and two
of them are genuinely reusable:

- `scan_controller._run_scan_loop` — the move / wait / settle / capture
  sequence, with background threading, `MultiThreadedExecutor` and interruptible
  sleeps. The production `scan_planner` is built on this.
- `motor_controller.normalise_angle` / `angle_difference` — correct
  shortest-path angle maths, already covered by 57 passing tests.
- The URDF stand model and `display.launch.py`.

**What is replaced, and why.** All three nodes used `std_msgs`/`std_srvs`
only, with no custom types, no action servers, no limits and no fault
detection. `package.xml:36-39` states this was deliberate ("using
`std_srvs/Trigger` for simplicity"). The target architecture needs typed
interfaces, homing, ramping, stall detection and an e-stop, none of which fit
in a `Trigger`.

---

## Not archived, and why

**`ui/app.py` (Streamlit, 713 lines).** Still referenced by the README as the
operator workflow and it genuinely works. It is superseded by the W7 dashboard,
at which point it moves here. It is not deleted now because it is the only
working UI and removing it would leave an operator with nothing.

**`attendance.db`, `data/`, `ENROLL_PHOTOS/`.** Untouched on disk. They are
biometric data and removing them is a decision for a human, not a refactor.
See `docs/HUMAN_ACTIONS.md` item 4.
