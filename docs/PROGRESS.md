# PROGRESS

**How to resume:** read this file, then `docs/00_audit.md` (the original
findings), `docs/assumptions.md` (the operator's fixed decisions supersede it),
and `docs/HUMAN_ACTIONS.md` (everything only the human can do).

**Branch:** `feature/industrial-hardening`
**Started:** 2026-09-29
**Rule:** update this file at the end of every workstream. A fresh session must
be able to continue without asking anything.

---

## Status at a glance

| WS | Workstream | Status |
|---|---|---|
| W1 | Repo hygiene, safety, tooling, Alembic, CI | ✅ DONE |
| W2 | Correctness fixes from the audit | ✅ DONE |
| W3 | Pure core + interfaces | ✅ DONE (ports, types, domain, vector index, identity engine, perception pipeline) |
| W4 | Multi-tenant data model + auth/RBAC | 🟡 PARTIAL (tenant-scoped auth/RBAC, consent, audit, roster, ingestion and API tests exist; production identity/policy decisions remain) |
| W5 | Edge ROS 2 Jazzy packages | 🟡 PARTIAL (7 packages build and 259 edge tests pass; simulated 16-frame sweep recorded working; durable outbox and physical verification remain) |
| W6 | Cloud perception + identity engine | 🟡 PARTIAL (InsightFace batch path, calibration, data protocol, held-out evaluator and benchmark harness exist; liveness is not wired and real-data evidence is unavailable) |
| W7 | Continual learning + operator layer | 🟡 PARTIAL (unknown-cluster storage/listing and identity core exist; operator workflow, conversational API and gated metric lifecycle remain) |
| W8 | Attendance service + reporting | 🟡 PARTIAL (session close-out and JSON/CSV register exist; XLSX/PDF, timetable scheduler and webhook remain) |
| W9 | Security, privacy, compliance | 🟡 PARTIAL (consent, retention, erasure and S3 SSE-KMS adapter exist; deletion verification, key lifecycle and legal/compliance approval remain) |
| W10 | Observability + reliability + fault injection | 🟡 PARTIAL (Prometheus-style metrics, health/readiness and request instrumentation exist; fault injection, tracing and debug visualizer remain) |
| W11 | Deployment (Docker, Terraform, edge installer, cost) | 🟡 PARTIAL (Docker/Compose exist; Docker is single-stage and Terraform, edge installer and cost model are absent) |
| W12 | Evaluation, benchmarks, docs | 🟡 PARTIAL (focused detector/channel measurements and a held-out verification evaluator exist; synthetic classroom generator and LIMITATIONS.md remain) |

## Re-audit — 2026-09-30

The original W1–W3 notes and W5 follow-up entries below are historical work records. The current
status table reflects the source tree as it exists now; see the current re-audit in
`docs/00_audit.md` for the evidence and boundaries. Do not infer that a workstream is complete
from an earlier section describing one passing component or one successful simulated run.

### Immediate W6 work

- The working tree already contained calibration logic, the database score collector, a CLI
  script, liveness placeholders, an S3 SSE-KMS adapter, and the batched perception path. Those
  files were not committed when re-audited.
- `tests/test_w6_calibration_data.py` initially exposed fixture defects: seeded attendance
  events were never added to the session, and committed rows collided across tests. Both are
  fixed; the module passes **8 tests**.
- `docs/data_collection_protocol.md` now specifies consent, session-separated splits, score-file
  provenance, retention and deletion verification. `scripts/evaluate.py` selects a threshold on
  calibration sessions and measures the fixed threshold on held-out test sessions.
- Synthetic evaluator tests pass, but there is no consented real held-out score file. No TAR@FAR
  claim should be made about the project's real-world attendance performance.
- `scripts/benchmark_pipeline.py` runs the configured perception path on explicitly supplied
  images and reports aggregate p50/p95 stage latency and coverage without writing image data or
  paths. Its real-world run remains blocked on consent-approved inputs.
- Liveness classes are registry placeholders only; `app/pipeline/perception.py` does not consult
  them, and no shipped backend performs anti-spoofing. Report real-data metrics only when the
  human actions in `docs/HUMAN_ACTIONS.md` provide consented held-out samples.
- Final verification: cloud suite **431 passed, 4 warnings**; ROS workspace **7 packages built,
  259 tests passed**. `ruff check app tests scripts` passes. Repository-wide formatting still has
  15 files to normalize; `mypy app` has 10 legacy errors in `app/api/routes.py`, while the
  typing-ratchet tests pass.

---

## W1 — Repo hygiene, safety, tooling, CI — **DONE**

### Done

**Safety (the urgent part)**
- `.gitignore` and `.dockerignore` added. `.dockerignore` specifically stops the
  original `COPY . .` from baking `.env` + 850 MB of face crops into images.
- 581 files `git rm --cached`-ed: `.env`, `ENROLL_PHOTOS/` (39 real faces),
  `data/` (496 crops + frames), `DL_PROJECT.zip` (178 MB), `dl.zip` (486 MB),
  `ui/session_history.json`, all `__pycache__`. **Files remain on disk** —
  verified 496 data files and 39 enrollment photos still present.
- Git **history** still contains the data. The purge is prepared but NOT run:
  `docs/HUMAN_ACTIONS.md` item 3 (history rewrite = irreversible).

**Configuration**
- `app/core/config.py` rewritten. No secret defaults. `validate_invariants()`
  collects every problem and reports them together.
- Production now **refuses** a dev API key, a short key, a missing JWT secret,
  `STORAGE_BACKEND=local`, `JOB_QUEUE_BACKEND=memory`, and missing
  `S3_KMS_KEY_ID`. `staging` counts as production. `Production`/`  PRODUCTION `
  are normalised so a typo cannot bypass the guard.
- `.env.example` (documented, no values), `scripts/generate_secrets.py`
  (CSPRNG, refuses to overwrite without `--force`, chmod 600).

**Alembic is now the only schema path**
- `migrations_alembic/` → `alembic/`; the stub `migrations/001_initial.sql`
  archived to `archive/legacy_migrations/`.
- `init_db()` / `create_all()` removed from the production path. `main.py`
  calls `assert_no_tables_in_production()`.
- VERIFIED: `alembic upgrade head` works, `alembic check` reports
  "No new upgrade operations detected", and downgrade→upgrade round-trips.
- ORM models moved to `app/models/schema.py`; `database.py` owns the engine.

**Tooling**
- `pyproject.toml`: ruff (14 rule families incl. bandit `S`), ruff-format, mypy
  (strict-ish), pytest markers, coverage config.
- `ruff check app tests scripts` → **All checks passed** (was 119 errors).
- Dependencies pinned exactly from `pip freeze` (ADR 0002).
- `.pre-commit-config.yaml` incl. a model-weight-hash hook.
- `.github/workflows/ci.yml`: cloud job (lint/format/mypy/pytest/Alembic/
  licence-guard/secret-scan), edge job (ROS 2 Jazzy colcon), security job.

**Model licensing (the production blocker)** — see `docs/model_licensing.md`
- `app/registry/`: `ModelRegistry`, `LicenseMetadata`, `ModelDescriptor`.
- Backends: `opencv_yunet_sface` (MIT + Apache-2.0, the shippable baseline),
  `insightface_buffalo_l` (flagged non-commercial, dev/benchmark only),
  `licensed_stub` (drop-in slot, raises loudly).
- Weight SHA-256s recorded and verified by `scripts/verify_model_hashes.py`.
- **Production guard**: 20 tests, adversarial. VERIFIED:
  `ENVIRONMENT=production DETECTOR_BACKEND=insightface_buffalo_l python -m app.cli check_licensing`
  → exit 1. With `opencv_yunet`/`opencv_sface` → exit 0.
- One deliberate trade recorded: SFace's undocumented training corpus is an
  **advisory**, not a blocker (otherwise nothing can ship). Pinned by a test.

**Interfaces (W3 groundwork, landed early because `main.py` needs the registry)**
- `app/core/domain/types.py` — framework-free value types.
- `app/core/interfaces/ports.py` — Detector, Embedder, LivenessChecker,
  VectorIndex, ObjectStorage, Clock, Camera, Servo, JobQueue.

**Other**
- `app/retention.py`: retention for **all four** image classes, fixing the
  audit gap where `review-context` images were never purged. Deleting an image
  nulls the evidence column; the audit row survives. Dry-run by default.
- `app/cli.py`: `doctor`, `check_config`, `check_licensing`, `models`, `purge`,
  `reindex` — actionable output instead of tracebacks.
- ADRs 0001–0004 (edge/cloud split, pinning, protocol, hexagonal core).
- `pytest` at repo root now works with no ROS (was a hard collection failure).

### Test results

```
$ .venv/bin/python -m pytest -q
47 passed, 1 warning in 1.35s

$ ruff check app tests scripts
All checks passed!

$ ruff format --check app tests scripts
(clean)
```

23 of the 47 are the original tests, all still passing — including the
behavioural ones the brief requires preserved: manual label outranks auto,
unconfirmed ≠ present, review resolve/dismiss/reopen reversible, and the DB
surviving a FAISS failure.

### What W1 did NOT do
- History rewrite (irreversible → HUMAN_ACTIONS).
- mypy is configured but **not yet clean** — the legacy modules still lack type
  annotations. Tracked as a W3 item.
- No secrets rotated yet (needs the human).

---

## W2 — Correctness fixes from the audit — **DONE**

### Done, with measurements

**The image ingestion boundary** (`app/core/domain/imageops.py`) — the single
place images are decoded. Fixes audit 4.1 and 4.2 at the root.

| Fix | Evidence |
|---|---|
| **4.1 BGR channel order** | **MEASURED, paired, 4 students / 23 photos / 253 pairs.** Separability **+0.2893 → +0.3679** (+27%). Same-person p05 **0.121 → 0.404**. See `docs/benchmarks.md` §1. Reproduce: `python scripts/measure_channel_order.py` |
| **4.2 EXIF orientation** | All 8 cases tested, including a **pixel-content** check (a corner marker must move), not just dimensions. 10 tests. |
| **4.8 det_score floor + quality gate** | 3-tier: REJECT / POOR / GOOD. A 50 px face is matchable but **cannot auto-confirm**, and requests a zoom re-capture. Previously `det_score` was captured and never used. |
| **4.10 evidence = aligned crop** | The stored evidence is now the 112×112 warp the embedder consumed, not a raw box slice. Asserted in tests. |

**A real perf bug found by measurement, not by reading.** The first
`YuNetDetector` called `setInputSize((width, height))`, silently overriding the
configured working size — so the detector ran at full 12 MP. `scripts/sweep_detector.py`
measured the cost: **6× latency and 9× false positives for zero recall gain**
(1280/0.60: 1.58 FP/img, 153 ms vs 320/0.70: 0.17 FP/img, 26 ms). Fixed by
downscaling to a working size and mapping boxes back. Pinned by
`test_working_size_is_not_ignored`.

**Decision engine** (`app/core/domain/decision.py`) — fixes 4.3.
- k=1 argmax replaced by score + **margin** + **roster prior**.
- `REASON_BETWEEN` added because the first draft reused `below_low_threshold`
  for both "matched nothing" and "matched unconfidently", making the column
  useless for calibration.
- Runner-up is always a **different identity**, so a multi-exemplar gallery does
  not make every match look ambiguous.
- The project's own documented failure (R1 0.632 vs R3 0.631) is a test.

**Dedup** (`app/core/domain/dedup.py`) — fixes 4.5. Framework-free clustering,
O(n·k) over cluster count, **zero database access**. The legacy `_is_duplicate`
re-queried the pending-review table and re-unpacked every embedding once per
face. Purity is enforced by an AST test.

**Attendance** (`app/core/domain/attendance.py`) — fixes 4.6.
PRESENT / ABSENT / **UNVERIFIED**, with a configurable presence rule
(`once` / `times` / `confirmed`) and a `required_distinct_angles` knob.

**Session close-out** (`app/core/domain/session.py`) — fixes 4.9. Idempotent
close, watchdog sweep, reason recorded. 9 of 11 legacy sessions had a NULL
`end_time`.

**Job queue** (`app/core/domain/jobs.py`) — fixes 4.7. Bounded, idempotent,
retrying, with an explicit concurrency bound replacing the 40-thread AnyIO
pool that hammered one ONNX session.

**New perception pipeline** (`app/pipeline/perception.py`) — tiles → detect →
quality → align → batch-embed, returning faces, rejections **with reasons**, and
recapture regions.

### Bugs my own tests found (all fixed)

Writing the tests first was worth it — these were all mine:

1. **Manual override was silently ignored.** `classify()` returned ABSENT
   before checking `manual_override`, so a teacher marking an absent-looking
   student present had no effect. The override is now applied first.
2. **Tile cap off by one.** A 4×4 grid plus the full-frame pass produced **17**
   detector calls under a 16-tile cap.
3. **NMS let artefacts through.** A 4 px box inside a 100 px box has IoU
   0.0016, so the overlap-only artefact check never fired.
4. **Job dedup never fired.** `_in_flight` is keyed by `job_id`, not
   `dedup_key`, so the membership test never matched and five redeliveries of
   the same frame ran five times. Replaced with a single `_seen` map reserved
   at enqueue.
5. **Tiling regressed small frames.** The new pipeline tiled unconditionally,
   doubling detector work on every 640×480 frame.
6. **W1 left `recognizer.py` broken at runtime** — it used settings fields W1
   had removed. mypy caught it. Now a shim over the registry, so it inherits
   the licence guard.

### Test results

```
$ .venv/bin/python -m pytest -q
206 passed          (was 51 at end of W1; +155 this workstream)

$ ruff check app tests scripts      -> All checks passed!
$ ruff format --check               -> clean
$ mypy app                          -> 32 errors, all in the 2 legacy
                                       files W3 restructures; ratcheted
```

All 23 original behavioural tests still pass: manual label outranks auto,
unconfirmed ≠ present, reversible review actions, DB survives FAISS failure.

### Measured on real 4K classroom photos (MEASURED)

```
IMG_...143415.jpg:  1021ms  detected=2 usable=2 rejected=0 recapture=0 largest=955px
  timings: decode=345ms detect=382ms quality_align_embed=147ms
```

**The pipeline is dominated by decode and detect, not embedding** (~96% of the
time). Recognition was never the bottleneck; face *location* is. That reframes
where optimisation effort belongs.

### Still UNVERIFIED (and labelled as such in docs/benchmarks.md)

TAR@FAR, FAR, FRR, coverage %, duplicate rate, unknown-rate trend, end-to-end
scan time, GPU figures. No evaluation set exists. Protocol in
`docs/data_collection_protocol.md`; GPU run in HUMAN_ACTIONS item 6.

### Known diagnostic gap

Detector recall caps at **0.75** on the portrait set and does not improve with
working size — 6 of 24 portraits found no face. Cause **not diagnosed**;
extreme pose or blur is a hypothesis, not a finding. Tracked in
`docs/LIMITATIONS.md` (written in W12).

---

## W3 — Pure core + interfaces — **DONE**

### Done

**Vector index** (`app/services/vector_index.py`) — replaces the legacy flat
FAISS wrapper with a per-identity exact search.

- **One result per identity, not per vector.** The legacy index searched k=1
  over raw vectors, so a student with 20 enrollment photos occupied 20 rows and
  the odds the top hit was *them* rather than the next student were 20-to-1 at
  equal true similarity. This is the mechanism behind the audit's imbalance
  concern, and it is now correct by construction.
- **Gallery depth is exposed.** `IdentityMatch.exemplar_count` surfaces the
  R1=131 / R4=1 asymmetry (audit 4.4) as data rather than a footnote.
- **Search is per-identity top-k**, because the margin rule needs a runner-up
  and a runner-up must be a *different* student, not that student's second-best
  exemplar.
- **Roster is a query filter**, so an out-of-roster candidate is never scored.
- **MEASURED** on the CI machine: 4,500 vectors (300 students x 15 exemplars,
  128-d) searched in **< 10 ms**. Exact search is the right choice at this
  scale; FAISS stays behind the same port for >10^5.
- Dimension mismatch raises with an actionable message rather than silently
  mixing embedding spaces.

**Identity engine** (`app/services/identity.py`) — the "brain".

- Orchestrates index search + the three decision rules + the quality gate.
- **Gallery-depth gate**: a match on a student with fewer than
  `MIN_EXEMPLARS_FOR_AUTO` (3) is demoted CONFIRMED → UNCERTAIN, because a
  nearest-neighbour score is an order statistic over exemplars and a
  one-exemplar student is systematically harder to match than a hundred-
  exemplar one. Demotes only; never promotes.
- **Quality gate is a hard ceiling**: a poor face can be *proposed* to the
  operator but can never be auto-confirmed.
- `resolve_session()` does what the legacy system could not: cross-frame
  clustering → per-student evidence → PRESENT/ABSENT/UNVERIFIED.
- `unknown_summary()` produces the exact conversational opening the brief
  asks for.

**`_is_duplicate` fixed properly** (audit 4.5). The first attempt used a cache
keyed on the pending count — which meant it had to *query* to know whether its
own cache was valid, i.e. it kept the cost it was meant to remove. Replaced
with `PendingReviewIndex`, built **once per frame** by the processor that
knows the frame boundary. A test that counts `query()` calls now proves
one query per FRAME, never per face.

**Archive** (`archive/README.md`) — every removed behaviour is listed with the
module that replaced it and why. Nothing is deleted; the ROS package's
reconciliation is documented there too.

### Tests: 257 passed (was 206 at end of W2; +51)

`tests/test_identity_engine.py` (43) and `tests/test_w3_performance.py` (8) are
new, plus the original 23 still green.

### Two more real bugs the tests found

1. **A student proposed-but-never-confirmed was reported ABSENT.** We saw
   somebody and thought it was R1; claiming absence is a stronger statement
   than the evidence supports. `StudentObservation` now tracks candidate
   sightings separately, which is what makes UNVERIFIED reachable.
2. **The time-based dedup cache was ineffective** (above).

---

## W4/W5 status correction

The W4 implementation and the ROS workspace now exist, so the old ``Next: W4`` and “workspace
needs to be created” notes are superseded. W4 has tenant-aware API, consent, audit, class roster,
ingest and session-close paths with tests. W5 has edge packages and a simulated sweep recorded as
working. Remaining work is integration, production verification and the explicitly human-only
hardware/legal/data actions; neither workstream should be marked done yet.

---

## W5 -- Edge ROS 2 workspace: PARTIALLY COMPLETE

**Status: 6 of 8 packages complete and verified. A full end-to-end sweep does
NOT yet run. Read "what is not done" before assuming it does.**

### Verified working

| Component | Evidence |
|---|---|
| 7 packages build | `./build.sh` -> "7 packages finished" |
| 255 ROS tests pass | `colcon test` -> 255 tests, 0 failures, 0 skipped |
| 330 cloud tests pass | unchanged from W4 |
| Edge lint clean | separate `ros_ws/pyproject.toml` |
| 4 nodes start together | `ros2 launch ... mode:=simulated` -> 0 crashes |
| Live camera capture | real service round trip: 4608x3456, sha256 returned, sharpness measured |
| Live servo move | real action round trip: -18.5 deg in 504 ms, `SUCCEEDED` |

`ros_ws/src/attendance_mocks/` preserves the original package; its 57 tests
still pass.

### The hardware finding that drives the design

At 70 deg FOV and 4608 px, a phone produces **62 px of face at 8 m** against an
80 px identification floor. The back of a lecture hall cannot be identified at
1x, and **digital zoom cannot fix it** -- interpolation adds no information and
smooths exactly the detail a face embedding keys on. The camera needs a
motorised **optical** telephoto. Reproduce with
`ros2 run scan_planner show_face_sizes --room 12 9`.

This is derived from a documented model, not measured on hardware. The inputs
are plausible phone values. See `docs/hardware/pixels_per_face.md`.

### What is NOT done

1. **A sweep now MOVES through all 16 steps, but captures are unreliable.**
   The `servo_unavailable` blocker is fixed (see below): the sweep plans, moves
   the mechanism to each angle, and steps through the whole plan. But only the
   FIRST capture request reaches the camera; the rest time out client-side.

   Cause: the execute callback uses
   `rclpy.spin_until_future_complete(self, future)` to wait for service and
   action replies, while `main()` is already running `executor.spin()` on the
   same node. rclpy does not support spinning a node that another executor is
   already spinning; it works for the first request and then races.

   The fix is to make the execute callback a **coroutine** so rclpy's
   `await_or_execute` awaits it and the futures are awaited rather than
   re-spun. An earlier attempt at this failed with
   `RuntimeError: no running event loop` because the helper used
   `asyncio.sleep`; the correct form is to `await` the rclpy future directly.
   **This is the next thing to do.**
2. **No edge face detector.** `assess_frame` needs face boxes, so the edge
   currently checks resolution and sharpness only, and the cloud remains the
   authoritative quality and identity gate. Calling `assess_frame` with an
   empty box list would reject every frame and report zero captures while the
   sweep looked healthy, so that is deliberately not done.
3. **No rosbag fixtures** for the sweep.
4. **The uploader has never run against a real API.** Its logic is unit
   tested; no server was available.
5. `IpWebcamDriver` is **unverified against any phone app**. The operator has
   not confirmed which app they use.

### Bugs found by the tests and by the end-to-end run

Unit tests (11): the FOV/zoom validation used linear zoom instead of
`atan`; the frame-gap had a spurious factor of two; the tele pass generated
798 steps for a 12x9 m room; angles too distant to detect were never queued
for a tele retake, so a 20x18 m room could not be scanned at all; wide-pass
gating on the identification floor discarded the frames that show *where* to
point the tele lens; `pending_count()` was inverted; `QueueFull` was
unreachable because the just-enqueued capture was its own eviction candidate,
so a too-small budget was silently exceeded; `httpx` is not present in a
stock ROS Jazzy install, so the real-hardware camera path would have failed in
a classroom.

End-to-end run (8), none of which unit tests could have caught: every ROS
action callback used `goal_handle.feedback` and `goal_handle.result`, which
`ServerGoalHandle` does not have -- so **every move aborted instantly**; the
`GoToAngle` result had `success` and `error_message` commented out in the
`.action` file; `CaptureStill` put `sha256`/`metadata` in the *request* and
`captured_at` where the caller had to invent it, so a hash could never be
returned at all; `CaptureStatus` had no `DEGRADED` constant, silently folding
a warning state into `CONNECTING`; `scan_planner` called `/servo/go_to_angle`
but the servo registers `/stand/goto_angle`; the `edge_uploader` crashed on
`/var/lib/attendance` in any non-root run.

The pattern is worth stating plainly: **the driver logic was well tested and
the ROS wiring was untested, and the wiring was where every integration bug
was.** The servo package shipped in W5 part 1 with 55 passing tests and could
not move the mechanism once.


---

## W5 follow-up: the sweep now moves (blocker fixed, one defect left)

**The `servo_unavailable` blocker recorded above is FIXED.** A sweep now plans,
moves the mechanism to every angle, and steps through the entire plan. Verified
by running it: 16 steps, servo reached each commanded angle, the sweep
terminated with a report rather than hanging.

### Root cause, and it is a lesson about rclpy

`scan_planner` created its `ActionClient` in `__init__`, which runs at launch
time -- before the executor starts spinning and before `servo_controller` has
advertised itself. rclpy resolves a client's graph membership **at
construction**, so that client cached an empty answer and reported the server as
unavailable for the lifetime of the process, even though the server was running
and answered `ros2 action send_goal` perfectly. The client is now created per
sweep (`_fresh_goto_client`).

Four more API mistakes on the same path, each found by running the thing:

- `Client` has no `wait_for_service_async`, and this Jazzy build's
  `ActionClient` has no `wait_for_server_async` either. Both are poll loops.
- `send_goal()` **blocks and returns the `GetResult_Response` directly**. It
  does not return a `ClientGoalHandle`, so there is no `.accepted` and no
  `.get_result()` on it.
- The GetResult status byte is the full `action_msgs/GoalStatus` enum, where
  `SUCCEEDED` is **4**, not 0. Assuming 0 made every successful move report
  `motion_status_4` -- a working feature hidden behind a permanent error.
- `FrameManifest` had no `notes`/`kept`/`pan_deg`/`zoom`/`retake_count`, so
  every frame report raised. Added: an operator debugging a bad attendance
  report needs to know where the camera was pointing and why a frame was
  dropped.

### The remaining defect

Only the first capture request reaches the camera; the rest time out. The
execute callback waits with `rclpy.spin_until_future_complete` while `main()`
is already spinning the same node, which rclpy does not support. Fix: make the
callback a coroutine so rclpy awaits it and the futures are awaited directly
(no `asyncio.sleep` -- that is what produced `no running event loop` earlier).

### Also fixed, and worth keeping

A capture's success is keyed on an explicit `succeeded` flag, **not** on
`image is not None`. The image bytes deliberately do not travel in the ROS
response -- they live in the outbox and go to object storage -- so keying
success on bytes reported every good capture as a failure with an empty reason.

The sweep never finishes blank: any unexpected exception becomes
`fault_code: internal_error` with the exception text. That safety net caught
two of the bugs above on its own.


## W5 follow-up 2: a full simulated sweep now runs end to end

```
frames_attempted: 16
frames_captured: 16
frames_rejected: 0
duration_s: 5.895
fault_code: ''
```

Four nodes launched with one command, no crashes. Suites: 255 ROS tests,
330 cloud tests, edge lint clean.

### Still not done

1. **A sweep does not yet write to the outbox.** The sweep captures and
   publishes a `FrameManifest`, but nothing enqueues the image to the durable
   `EdgeOutbox`, so the uploader has nothing to send. The outbox logic itself
   is well tested (51 tests) -- it is the WIRING that is missing, and it is
   the same wiring-shaped gap that this whole workstream keeps hitting.
2. **No edge face detector**, so the edge gates on resolution and sharpness
   only and the cloud remains the authoritative quality/identity gate.
3. **`IpWebcamDriver` is unverified** against any phone app.
4. **No rosbag fixtures**, and the uploader has still never met a real API.
5. **The `servo_controller` result-type bug class is worth guarding.** Three
   separate action-callback defects (`.feedback`, `.result`, and a result
   message with its fields commented out) shipped with 55 passing tests,
   because the tests covered the driver and not the ROS wiring. An
   integration smoke test that starts all four nodes and drives one capture
   and one move would have caught all three, and would have caught the camera
   crash too. That is the first thing to add in W6.
