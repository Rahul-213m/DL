# AI Classroom Attendance System

A FastAPI + InsightFace system that marks attendance from group photos.
The face-recognition model is **never retrained** — you only add labeled photos and tune two number thresholds.

---

## How to run

From the project root, create the local environment and database once:

```bash
cd ~/Documents/DL_PROJECT
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -c "from app.models.database import init_db; init_db()"
```

Start the API in terminal 1:

```bash
cd ~/Documents/DL_PROJECT
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Start the UI in terminal 2:

```bash
cd ~/Documents/DL_PROJECT
source .venv/bin/activate
streamlit run ui/app.py --server.address 127.0.0.1 --server.port 8501
```

Open http://127.0.0.1:8501. The API is available at http://127.0.0.1:8000.

After changing `.env` (especially either confidence threshold), stop and restart the API. The
development reloader watches Python source files, but it does not reliably reload environment settings.

---

## What happens inside — step by step

### 1. Enrollment

You give the system 8–15 clear, single-face photos of each student.

For each photo the system:
1. Runs **InsightFace `buffalo_l`** (a pre-trained ArcFace model) to detect the face
2. Extracts a **512-dimensional embedding** — a list of 512 numbers that uniquely describes that face
3. Stores the embedding in the **SQLite database** (`face_gallery` table) linked to the student's roll number
4. Adds it to an **in-memory FAISS index** for fast similarity search

The model weights never change. Only the gallery of embeddings grows.

```
Photo → InsightFace → 512-number embedding → stored in DB + FAISS index
```

### 2. Capture (group photo)

You upload a classroom photo. The system:

1. **Detects every face** in the image using InsightFace
   - For large images (>2500px), it tiles the image into overlapping quadrants and merges results to catch small faces
   - Faces smaller than 40px are discarded
2. For each detected face, **extracts its 512-number embedding**
3. **Searches the FAISS index** — finds the closest stored embedding using cosine similarity (a score from 0.0 to 1.0)
4. **Routes the match** based on two thresholds you control:

```
Score ≥ HIGH (default 0.70) → auto-present  ✅  recorded immediately, no human needed
Score ≥ LOW  (default 0.35) → review queue  🟡  human must confirm
Score < LOW                 → rejected      🔴  too uncertain, discarded
```

5. Saves a **face crop** and the **full frame** to disk as evidence
6. Processing runs in the background — the API responds immediately with 202 Accepted

### 3. Review Queue

For every face that landed in the review queue, the UI shows you:
- The cropped face
- The full frame with a red bounding box showing where the face was
- The confidence score and the system's best guess

You type the correct roll number (or click "Not a match") and submit.
When you resolve a face:
- The embedding is **added to that student's gallery** — the system learns from your correction immediately
- If the roll number is **not already enrolled**, a new `students` record is created on the spot (mid-semester enrollment via the review queue)
- An **audit event** is written to the database permanently (cannot be deleted)
- The FAISS index is updated in memory so the next capture benefits right away
Resolutions are persisted in the **database** (`face_gallery`), which is the source of truth; FAISS is
rebuilt from that table on startup. Every change that grows a student's gallery updates the database;
the first 15 images are also **mirrored into `ENROLL_PHOTOS/<roll_no>/`**. Once that local folder is
full, later embeddings remain in SQLite and are intentionally not written as additional local photos.
The mirror is content-addressed, so re-adding the same image never creates a duplicate file.

### 3b. Managing the gallery (no SQL required)

The UI's **Manage & Repair** tab (under *1 · Enroll*) lets any operator — DBMS knowledge not needed —
see and fix the enrollment state:

- **Student table** — each roll number and how many face embeddings the database holds for it
- **Consistency check** (`GET /system/consistency`) — lists every mismatch between the database and the
  `ENROLL_PHOTOS/` folders (a student with no embeddings, photos with no student, a stale count)
- **Repair** (`POST /system/repair`) — recomputes each student's embedding count from `face_gallery` and
  rebuilds the FAISS index
- **Re-import a student** (`POST /students/{roll_no}/reimport`) — rebuilds one student's gallery from the
  photos in `ENROLL_PHOTOS/<roll_no>/`. This is the remedy for a student whose enrollment never completed
  (photos on disk, no DB embeddings). At least 8 images with a detectable face are required; the rest are
  reported as `rejected_images`.

**The database is the source of truth.** Every accepted gallery change is stored in SQLite. The
human-readable `ENROLL_PHOTOS/<roll_no>/` mirror is de-duplicated by content hash and capped at 15
images per student; its count may therefore be lower than the database gallery count.

### 4. Threshold Playground

The two thresholds control the trade-off:
- **Raise HIGH** → fewer auto-accepts, more faces go to review (safer but more work)
- **Lower LOW** → more faces go to review instead of being rejected (catches more uncertain faces)

The Playground lets you drag sliders and see — without re-running detection — how many faces from the current session would move between buckets. When you click Apply it writes to `.env`. Restart the API for it to take effect.

---

## Project structure

```
app/
  api/routes.py          — all HTTP endpoints
  core/config.py         — reads .env settings
  core/security.py       — API key check
  models/database.py     — SQLAlchemy tables (students, gallery, sessions, events, review queue)
  pipeline/
    recognizer.py        — wraps InsightFace; detect() returns face crops + embeddings
    matching.py          — cosine_similarity() + route_match() (auto / confirm / review)
  services/
    gallery.py           — FAISS index; append_gallery(), gallery_index.search()
    attendance.py        — process_frame(): tiling, dedup, routing, DB writes
  storage/local.py       — saves images to data/ with timestamped filenames

ui/app.py                — Streamlit tester UI (5-step workflow)
ENROLL_PHOTOS/           — put <roll_no>/ folders here for bulk enrollment
data/                    — face crops, full frames, review context images
attendance.db            — SQLite database
.env                     — all configuration (thresholds, paths, API key)

Note: photographs that never produce a detectable face (side profiles, full-body or
overhead shots) are rejected at enrollment; a student needs at least 8 valid frontal
photos. Use *Manage & Repair → Re-import* to retry a student from their folder.
```

---

## Key concepts

**Cosine similarity** — measures how similar two face embeddings are. 1.0 = identical, 0.0 = completely different. In practice, same-person scores cluster around 0.6–0.9; different-person scores are usually below 0.4.

**Gallery** — the collection of known embeddings for a student. More photos = more robust matching. Resolving review items grows the gallery automatically.

**FAISS index** — an in-memory search structure that finds the nearest embedding in the gallery in milliseconds, even with thousands of entries. It is rebuilt from the database on every server startup.

**ArcFace / buffalo_l** — the pre-trained neural network inside InsightFace that converts a face image into a 512-number embedding. It was trained on millions of faces and is not modified here.

---

## Configuration (`.env`)

| Key | Default | What it does |
|-----|---------|-------------|
| `HIGH_CONFIDENCE_THRESHOLD` | `0.70` | Score above which a match is auto-accepted |
| `LOW_CONFIDENCE_THRESHOLD` | `0.35` | Score above which a match goes to review (below = rejected) |
| `API_KEY` | `changeme-dev-key` | Required header for every API call |
| `INSIGHTFACE_MODEL` | `buffalo_l` | InsightFace model package (downloaded automatically on first use) |
| `MIN_FACE_SIZE_PX` | `40` | Faces smaller than this are ignored |
| `TILING_THRESHOLD_PX` | `2500` | Images wider/taller than this get tiled for better small-face detection |
| `TILE_TARGET_SIDE_PX` | `1600` | Target tile size for dense classroom coverage; a 4K frame uses a 3×3 grid plus a full-frame pass |
| `MAX_DETECTION_TILES` | `16` | Hard cap on tile inference calls per frame |
| `MAX_IMAGE_PIXELS` | `36000000` | Rejects decompression-bomb images while allowing normal 4K captures |
| `RAW_FRAME_RETENTION_DAYS` | `30` | How long to keep raw frame images on disk |

---

## Production deployment requirements

The local `uvicorn --reload` and Streamlit commands are for development only.
For a real 90–120 student classroom deployment:

1. Use the supplied Docker Compose stack with PostgreSQL, set long random `API_KEY` and
   `POSTGRES_PASSWORD` environment variables, and set `ENVIRONMENT=production`. Startup
   intentionally fails if the development API key is used in production.
2. Use a dedicated GPU inference host. The CPU path works for asynchronous capture, but a
   4K classroom photo requires multiple detector passes and is not suitable for a busy
   multi-class deployment without capacity testing.
3. Use a licensed recognition model. The bundled InsightFace pretrained `buffalo_l` package
   has terms separate from the Python library; obtain the required model rights before
   commercial or institutional production use.
4. Run a labelled pilot set of at least three 90–120-student photos per room and lighting
   condition. Approve deployment only after verifying detection recall, false-auto-match
   rate, review workload, and end-to-end latency against your institution's acceptance
   criteria.
5. Establish consent, access controls, encrypted backups, a retention policy, and an
   incident process for biometric data. This application does not implement liveness
   detection, so do not use it where spoof resistance is required.

---

## Evidence and audit trail

Every face detection creates an `AttendanceEvent` row in the database with:
- the face crop path, full frame path
- the embedding (stored as bytes)
- the confidence score and match type (`auto` / `manual_label`)
- a timestamp

The original capture event is retained. If an operator undoes a review decision, the event returns to the pending queue and the gallery embedding added by that decision is removed; no separate `REVERTED` event is created.

Run `python scripts/purge_old_frames.py` (e.g. daily via cron) to delete old image files while keeping all database records intact.

---

For the verified fresh-clone startup and integration flow, see [docs/INTEGRATION.md](docs/INTEGRATION.md).

For internet deployment, device provisioning, secure ROS-to-cloud frame uploads, session handoff,
offline recovery, and production gates, see [docs/EDGE_CLOUD_DEPLOYMENT.md](docs/EDGE_CLOUD_DEPLOYMENT.md).

---
