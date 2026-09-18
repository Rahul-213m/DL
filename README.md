# AI Classroom Attendance System

A FastAPI + InsightFace system that marks attendance from group photos.
The face-recognition model is **never retrained** — you only add labeled photos and tune two number thresholds.

---

## How to run

```bash
# Terminal 1 — API
cd ~/Documents/DL_PROJECT
source .venv/bin/activate
uvicorn app.main:app --reload
# API running at http://127.0.0.1:8000

# Terminal 2 — Tester UI
source .venv/bin/activate
streamlit run ui/app.py
# Open http://localhost:8501 in your browser  ← the UI is here, NOT port 8000
```

First run only (if starting fresh):
```bash
pip install -r requirements.txt
python -c "from app.models.database import init_db; init_db()"
```

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
Score ≥ HIGH (default 0.55) → auto-present  ✅  recorded immediately, no human needed
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
rebuilt from that table on startup. Resolution does **not** write a copy into `ENROLL_PHOTOS/<roll_no>/`
— that folder is only an input for the one-time bulk `import-folders` step. A correction therefore
survives a server restart even though nothing is added to `ENROLL_PHOTOS`.

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
| `HIGH_CONFIDENCE_THRESHOLD` | `0.55` | Score above which a match is auto-accepted |
| `LOW_CONFIDENCE_THRESHOLD` | `0.35` | Score above which a match goes to review (below = rejected) |
| `API_KEY` | `changeme-dev-key` | Required header for every API call |
| `INSIGHTFACE_MODEL` | `buffalo_l` | InsightFace model package (downloaded automatically on first use) |
| `MIN_FACE_SIZE_PX` | `40` | Faces smaller than this are ignored |
| `TILING_THRESHOLD_PX` | `2500` | Images wider/taller than this get tiled for better small-face detection |
| `RAW_FRAME_RETENTION_DAYS` | `30` | How long to keep raw frame images on disk |

---

## Evidence and audit trail

Every face detection creates an `AttendanceEvent` row in the database with:
- the face crop path, full frame path
- the embedding (stored as bytes)
- the confidence score and match type (`auto` / `manual_label`)
- a timestamp

This row is **never deleted** — even if you undo a review resolution. Undo works by writing a second resolution event marked `REVERTED`, so the full correction history is always preserved.

Run `python scripts/purge_old_frames.py` (e.g. daily via cron) to delete old image files while keeping all database records intact.
