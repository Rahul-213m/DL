# LLM Build Prompt: AI Classroom Attendance Monitoring System

*Copy everything below the line into your LLM / coding agent (e.g., Claude Code) as the task prompt.*

---

## ROLE

You are a senior AI/backend engineer building a **production-grade, deployment-ready** classroom attendance monitoring system. Treat this as a real software delivery — with proper project structure, error handling, tests, documentation, and configuration management — not a notebook prototype. Write clean, modular, well-commented code. Do not skip error handling or take shortcuts that wouldn't survive a code review.

## PROJECT SUMMARY

Build the **AI/software core** of a classroom attendance system. A camera captures a photo of the **entire classroom** (a group shot containing many students, not individual walk-up captures) every few minutes across a 30-minute class session. The system must:

1. Detect and recognize **every face present in each group photo simultaneously**.
2. Aggregate recognition results across multiple frames in the session window to build a "present" list.
3. **Flag any face it cannot confidently recognize**, show it to a human operator (cropped face image + bounding box on the full frame), accept a manual roll-number label, and **incorporate that labeled face into its database** so recognition improves over time — without retraining the underlying deep learning model.
4. Support **querying by roll number**, returning not just present/absent status but the **actual face image captured during that session** as evidence, with timestamp and confidence score.
5. Compute the final **absentee list** = enrolled roll numbers − roll numbers seen during the session.

Hardware/camera-triggering integration is out of scope for this build — assume frames arrive as image files/uploads. Focus entirely on the AI pipeline, backend, database, and API/UI needed to run this end-to-end on pre-captured or uploaded classroom images.

---

## FUNCTIONAL REQUIREMENTS

### 1. Student Enrollment
- Accept 8–15 images per student at enrollment time (varying angle/lighting/expression).
- Detect and align faces, generate embeddings, store as that student's initial **embedding gallery** (not a single embedding).
- Reject enrollment images where no face or multiple faces are detected, with a clear error message identifying which image failed and why.

### 2. Session & Frame Capture
- A "session" represents one 30-minute class period, tied to a class/section ID.
- Accept multiple frame uploads (full classroom photos) during the session window.
- Each frame must be processed asynchronously (do not block the caller while detection/recognition runs).

### 3. Multi-Face Detection & Recognition (per frame)
- Detect **all faces** in a single classroom-wide group photo — must handle many faces per frame at varying scale, angle, and partial occlusion, including small/distant faces (back-of-room).
- Align each detected face and generate an embedding.
- Match each embedding against the enrolled gallery database using cosine similarity.
- Apply **three-tier confidence routing**:
  - High confidence (≥ configurable τ_high) → auto-mark that roll number as "seen" this session.
  - Mid confidence (τ_low–τ_high) → route to a **quick-confirm queue** with a best-guess roll number pre-filled for operator approval/correction.
  - Low confidence (< τ_low) → route to the **unrecognized-face review queue** with no pre-filled guess.
- Deduplicate: if the same unresolved face appears across multiple frames within one session, do not create redundant review entries for the same person — deduplicate by embedding similarity within the session before queuing.
- **Every single match event (auto, confirmed, or manually labeled), must persist the source face crop image**, timestamp, frame reference, and confidence score — this is required later for evidence-backed querying. Do not store just a boolean.

### 4. Unrecognized/Low-Confidence Face Review (Human-in-the-loop)
- Provide an API (and a minimal UI, see UI section) that:
  - Lists all pending review items for a session, each with: cropped face image, full-frame image with bounding box drawn around that face, detector/recognition confidence, timestamp.
  - Accepts an operator-submitted roll number to resolve an item.
  - On resolution: if the roll number exists, **append this embedding to that student's existing gallery**; if it does not exist, create a new student record with this as the first gallery entry (mid-semester enrollment case).
  - Incrementally updates the vector index (no full rebuild per label) and marks the roll number "seen" for the active session.
  - Logs operator identity and resolution timestamp for every manual label (audit trail).
  - Supports batch review — a single classroom frame can produce several unresolved faces at once; the UI/API must handle this as a queue/stack, not one-at-a-time only.

### 5. Query with Visual Evidence
- Given a session ID and roll number, return:
  - Status: present / absent.
  - If present: the **actual stored face crop from that session** (not the enrollment photo), timestamp of capture, frame reference, confidence score, and whether it was auto-matched or manually resolved.
  - If absent: explicitly state absent; optionally allow the operator to browse all frames from the session for manual visual verification.

### 6. Absentee Report
- Given a session ID, return the full list of enrolled roll numbers not present in the "seen" set, plus a full attendance summary (present/absent/manually-resolved counts).

### 7. Explicitly Required Design Constraint
- **Do not fine-tune or retrain the face recognition backbone model online.** "Learning" a newly labeled face must happen exclusively via gallery/index expansion (adding embeddings, incremental vector index updates), never via backpropagation on the deployed model. This is a hard requirement, not a suggestion — explain in your response if you believe this constraint should be relaxed, but implement it as specified.

---

## TECHNICAL STACK (use these unless you have a strong justified reason to deviate — state the reason if you do)

- **Language**: Python 3.11+
- **Face detection + recognition**: `insightface` library (RetinaFace for detection, ArcFace `buffalo_l` for embeddings)
- **Vector search**: FAISS, using `IndexIDMap` to support incremental `add()` without full rebuilds
- **Backend/API**: FastAPI, async endpoints, background tasks (or Celery + Redis if you judge the scale warrants a real task queue — justify the choice)
- **Database**: PostgreSQL for structured data (students, gallery metadata, sessions, attendance events, review queue) — SQLite acceptable for local dev, but schema/migrations should be Postgres-compatible
- **Image storage**: local filesystem under a structured directory for this build, but abstract it behind a storage interface so it can be swapped for S3/GCS later without touching business logic
- **Minimal UI**: a simple web UI (Streamlit is acceptable for speed, or a lightweight React page if you prefer) for: (a) the review queue (cropped face + bbox context + roll number input), (b) the query panel (roll number → evidence image), (c) a session dashboard showing live present/pending/absent counts

---

## DATA MODEL (implement as-is; extend only if needed and explain why)

- `students`: roll_no (PK), name, enrolled_at, gallery_embedding_count
- `face_gallery`: gallery_id (PK), roll_no (FK), embedding vector, source_image_path, added_via (`enrollment` / `manual_label` / `low_conf_confirm`), added_at
- `class_sessions`: session_id (PK), class_id, start_time, end_time
- `attendance_events`: event_id (PK), session_id (FK), roll_no (FK, nullable until resolved), face_crop_path, full_frame_path, confidence_score, match_type (`auto`/`manual_label`/`low_conf_confirm`), captured_at
- `review_queue`: review_id (PK), event_id (FK), status (`pending`/`resolved`), resolved_roll_no, resolved_by, resolved_at

---

## API ENDPOINTS (implement all; use proper request/response schemas with Pydantic, proper HTTP status codes, and OpenAPI docs via FastAPI's built-in support)

```
POST   /students/enroll                      multi-image upload, roll_no, name
POST   /session/start                        class_id -> session_id
POST   /session/{id}/capture                 upload one classroom frame -> triggers async pipeline
GET    /session/{id}/review-queue            list pending review items
POST   /review/{review_id}/resolve           { roll_no, resolved_by } -> gallery update
GET    /session/{id}/query/{roll_no}         status + evidence image + confidence
GET    /session/{id}/absentees               final absentee list + summary
GET    /session/{id}/status                  live present/pending/absent counts
POST   /session/{id}/end                     close session, finalize report
```

---

## NON-FUNCTIONAL REQUIREMENTS

- **Config management**: all thresholds (τ_high, τ_low), model paths, DB connection strings, storage paths must be in a config file/env vars — no hardcoded magic numbers in logic code.
- **Error handling**: every I/O operation (image read, DB write, model inference) must handle and log failures gracefully; the API should never return a raw stack trace to the caller.
- **Logging**: structured logging (e.g., via `logging` + JSON formatter) at each pipeline stage — frame received, faces detected (count), matches made, review items created, resolutions applied.
- **Testing**: unit tests for the matching/threshold logic and gallery update logic at minimum; integration test for the full capture → detect → match → review → resolve → query flow using sample images. Use `pytest`.
- **Performance**: document the expected latency per frame (detection + recognition for N faces) and note where batching or GPU inference would be needed at scale.
- **Security & privacy**: no public unauthenticated access to student images/embeddings; input validation on all uploads (file type, size limits); document a data retention approach for face images (raw frames should be purgeable after a configurable retention period while gallery embeddings persist).
- **Documentation**: a `README.md` with setup instructions, environment variables, how to run locally, how to run tests, and a description of the threshold calibration process (how τ_high/τ_low should be tuned on real data before go-live).

---

## DELIVERABLES / REPO STRUCTURE

Produce a complete, runnable repository with a structure similar to:

```
attendance-system/
├── app/
│   ├── api/                # FastAPI routers per endpoint group
│   ├── core/                # config, logging setup
│   ├── models/               # Pydantic schemas + DB models (SQLAlchemy)
│   ├── pipeline/            # detection, embedding, matching, dedup logic
│   ├── services/             # business logic: enrollment, review, query, reporting
│   ├── storage/              # storage abstraction (local now, S3-ready interface)
│   └── main.py
├── ui/                        # minimal Streamlit or React app
├── tests/
├── migrations/                # DB schema migrations
├── requirements.txt / pyproject.toml
├── .env.example
├── README.md
└── docker-compose.yml         # app + Postgres, for one-command local spin-up
```

---

## BUILD PROCESS — WORK IN THIS ORDER

1. Set up project scaffolding, config, DB models/migrations, and Docker Compose for local Postgres.
2. Implement the enrollment pipeline (detect → align → embed → store gallery) and its API/tests.
3. Implement the frame capture + multi-face detection/recognition pipeline with three-tier confidence routing.
4. Implement the review queue (list, resolve, gallery/index incremental update, dedup logic).
5. Implement the query-with-evidence and absentee report endpoints.
6. Build the minimal UI for review queue, query panel, and session dashboard.
7. Write unit + integration tests.
8. Write the README covering setup, running, testing, and threshold calibration guidance.

After each numbered step, briefly summarize what was built and flag any assumptions made or deviations from this spec before proceeding to the next step.

---

## ACCEPTANCE CRITERIA (the build is not done until all of these hold)

- [ ] A classroom group photo with multiple faces produces one detection+match attempt **per face**, not per-person sequential capture.
- [ ] Faces below τ_low appear in the review queue with both a cropped image and a bounding-boxed full frame.
- [ ] Resolving a review item updates that student's gallery and the FAISS index **without retraining any model**.
- [ ] Querying a present roll number returns the actual session-captured face image, not the enrollment photo.
- [ ] The absentee endpoint correctly returns enrolled roll numbers minus all roll numbers seen (auto or manually resolved) in that session.
- [ ] The same unresolved face appearing in multiple frames in one session does not create duplicate review entries.
- [ ] All thresholds are configurable, not hardcoded.
- [ ] Tests pass and the system runs end-to-end via `docker-compose up`.

---

*End of prompt.*
