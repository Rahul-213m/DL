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
| W2 | Correctness fixes from the audit | ⬜ NEXT |
| W3 | Pure core + interfaces | ⬜ (interfaces landed early in W1; domain logic pending) |
| W4 | Multi-tenant data model + auth/RBAC | ⬜ |
| W5 | Edge ROS 2 Jazzy packages | ⬜ |
| W6 | Cloud perception + identity engine | ⬜ (ModelRegistry + 2 backends landed in W1) |
| W7 | Continual learning + operator layer | ⬜ |
| W8 | Attendance service + reporting | ⬜ |
| W9 | Security, privacy, compliance | ⬜ (retention module landed in W1) |
| W10 | Observability + reliability + fault injection | ⬜ |
| W11 | Deployment (Docker, Terraform, edge installer, cost) | ⬜ |
| W12 | Evaluation, benchmarks, docs | ⬜ |

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

## Next: W2 — correctness fixes

Each gets a **failing regression test first**, then the fix, then a before/after
measurement on the sample images in `dummy_test/` and `ENROLL_PHOTOS/`.

| # | Fix | Audit ref |
|---|---|---|
| 1 | RGB→BGR channel order into InsightFace | §4.1 |
| 2 | EXIF orientation | §4.2 |
| 3 | k=1 nearest neighbour → k=2 + margin rule | §4.3 |
| 4 | `det_score` floor + real face-size target | §4.8 |
| 5 | Evidence crop = the aligned crop actually embedded | §4.10 |
| 6 | `_is_duplicate` per-face DB query | §4.5 |
| 7 | `absentees()` global roster → per-class roster | §4.6 |
| 8 | Unclosed sessions → close-out | §4.9 |
| 9 | `BackgroundTasks` → bounded job queue | §4.7 |

---

## Blockers

- **W5 needs the ROS workspace created at `ros_ws/`.** Verified: `~/ros_ws` does
  not exist; `/home/rahul/ros2_ws` is an unrelated ROS tutorial workspace
  (cpp_pubsub, turtle_shapes, urdf_tutorial). `attendance_robot/` is the only
  copy, so there is nothing to merge — it becomes the canonical `ros_ws/src/`.
- **W12 needs the AWS GPU benchmark.** Script + protocol to be written; the run
  itself is HUMAN_ACTIONS.
- **Nothing else is blocked.**
