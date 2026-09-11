# AI-Based Classroom Attendance Monitoring System
## Technical Blueprint & Deployment Specification (v2.0)

---

## 1. Purpose & Scope

This document defines the complete AI architecture for a camera-based classroom attendance system with three core capabilities:

1. **Automatic recognition** of enrolled students from a classroom photo, aggregated over a 30-minute session window.
2. **Human-in-the-loop handling of unrecognized faces** — the system flags any detected face it cannot confidently match, displays it to the operator with a bounding box, accepts a manual roll-number label, and updates its own database so it recognizes that person going forward.
3. **Evidence-backed querying** — when asked about a specific roll number, the system doesn't just return present/absent; it returns the actual cropped face image captured during that session as visual proof, with timestamp and confidence score.

Hardware integration (camera triggering, edge device selection) is explicitly out of scope for this phase, per requirements. This blueprint focuses entirely on the AI/software system.

---

## 2. System Architecture

```
                         ┌─────────────────────┐
                         │   Camera Frame Feed   │
                         │ (captured every 3-5   │
                         │  min during 30-min     │
                         │  session window)       │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │   Face Detection       │
                         │   (RetinaFace/YOLOv8)  │
                         └──────────┬───────────┘
                                    │  N face crops + bounding boxes
                         ┌──────────▼───────────┐
                         │  Alignment + Embedding │
                         │  (ArcFace / InsightFace)│
                         └──────────┬───────────┘
                                    │  512-D embedding per face
                         ┌──────────▼───────────┐
                         │  FAISS Similarity      │
                         │  Search vs Enrolled DB │
                         └──────────┬───────────┘
                     similarity ≥ threshold?
                    ┌───────Yes────┴────No────────┐
                    ▼                              ▼
        ┌───────────────────┐         ┌────────────────────────┐
        │ Mark roll_no as    │         │  UNRECOGNIZED FACE      │
        │ "seen" in session  │         │  QUEUE                  │
        │ + store face crop  │         │  - Save crop + bbox     │
        │   as evidence      │         │  - Save embedding       │
        └───────────────────┘         │  - Push to review UI     │
                                       └───────────┬─────────────┘
                                                    │
                                       ┌────────────▼─────────────┐
                                       │  Operator reviews image,  │
                                       │  enters roll number       │
                                       └────────────┬─────────────┘
                                                    │
                                       ┌────────────▼─────────────┐
                                       │  Enrollment Update:       │
                                       │  - Add embedding to       │
                                       │    gallery for that       │
                                       │    roll no (or create     │
                                       │    new student record)    │
                                       │  - Re-index FAISS         │
                                       │  - Mark present for        │
                                       │    current session         │
                                       └───────────────────────────┘

At query time:
  Absentees = Enrolled roll numbers − Seen roll numbers (this session)
  Query "roll no X" → return status + stored face crop(s) + timestamp + confidence
```

---

## 3. Core Design Decision: No Online Backbone Fine-Tuning

A critical architectural choice: **the recognition model (ArcFace) itself is never retrained live.** Retraining a deep embedding network on the fly from a single labeled image is unstable, slow, and risks catastrophic forgetting.

Instead, "learning" a newly labeled face works through **gallery expansion**, the same approach production face-recognition systems use:

- Each roll number maps to a **gallery of embeddings** (not just one), stored in the vector DB.
- When an operator labels an unrecognized face, its embedding is simply **added to that roll number's gallery** and the FAISS index is updated incrementally.
- At match time, a probe face is compared against *all* gallery embeddings for each identity, and the best score (or average of top-k) is used.
- This means accuracy for a given student **improves over time** as more labeled instances accumulate — different angles, lighting, days — without ever touching model weights.

This is simpler, safer, instantly effective, and standard practice — it should be presented to any evaluator as the correct engineering choice, not a shortcut.

---

## 4. Module Breakdown

### 4.1 Face Detection & Recognition Core
*(unchanged from prior phase — recap)*
- **Detector**: RetinaFace or YOLOv8-face — multi-face, small-face, angle-robust.
- **Recognizer**: ArcFace via `insightface` (`buffalo_l`), 512-D embeddings.
- **Alignment**: 5-point landmark warp before embedding.

### 4.2 Confidence Thresholding & Routing
- Cosine similarity ≥ **τ_high** (e.g., 0.55) → auto-accept match.
- Cosine similarity between **τ_low and τ_high** (e.g., 0.40–0.55) → route to a **"low-confidence review"** sub-queue (best-guess roll no shown, operator confirms or corrects — faster than full manual entry).
- Cosine similarity < **τ_low** → **unrecognized**, full manual labeling required.
- Thresholds are tunable hyperparameters — calibrate on your own enrollment data before go-live (see Section 8).

### 4.3 Unrecognized Face Handling Module
**Trigger**: any detected face falling below τ_low.

**Behavior**:
1. Crop the face region with padding (~20% margin) from the original frame.
2. Draw the bounding box **on a copy of the full class photo** as well, so the operator has spatial context of who's who in the room.
3. Push a record to the **Review Queue**:
   ```
   {
     review_id, session_id, timestamp,
     face_crop_path, full_frame_with_bbox_path,
     embedding_vector, detector_confidence,
     status: "pending"
   }
   ```
4. Present to operator via UI: cropped face (large) + full-frame context (small, with red circle/box) + input field for roll number.
5. On submission:
   - If roll number exists in DB → append embedding to that student's gallery.
   - If roll number is new → create new student record + initialize gallery with this embedding (first-time enrollment via the field, not just the formal enrollment phase).
   - Re-index FAISS (incremental add, not full rebuild — see 4.5).
   - Mark that roll number "present" for the active session.
   - Update `status: "resolved"` on the review record.

**Design note**: this queue-and-resolve pattern means the class photo capture and the recognition/labeling never block each other — recognition runs asynchronously, and the operator can resolve flagged faces at any point during or after the 30-minute window, before the final absentee report is generated.

### 4.4 Query & Evidence Module
**Trigger**: operator/user asks "Is roll no X present?" or "Show me roll no X."

**Behavior**:
1. Look up `roll_no` in the session's `seen_roll_numbers` table.
2. If present:
   - Retrieve the **actual face crop captured during this session** (not the enrollment photo) — this is the proof.
   - Return: status = Present, face image, timestamp of capture, matched confidence score, which frame number it was captured in.
3. If absent:
   - Return: status = Absent, plus (optionally) the last N frames' full images so the operator can visually spot-check if desired.
4. Every match — auto-matched or manually resolved — must store its source crop, so this evidence trail works uniformly regardless of how the identity was confirmed.

This requires that **every recognition event, not just unrecognized ones, persists its face crop image**, not just the roll number and a boolean. This is a storage design requirement, detailed in Section 5.

### 4.5 Incremental Index Update
- FAISS supports `index.add()` for incremental insertion without full rebuild — use `IndexIDMap` wrapping a flat or IVF index so embeddings can be tagged with `(roll_no, gallery_entry_id)` and added on the fly.
- Periodically (e.g., nightly), rebuild the index from the full database as a maintenance step to keep it optimally structured as galleries grow across many sessions.

---

## 5. Data Storage Schema

### `students`
| Field | Type | Notes |
|---|---|---|
| roll_no | PK, string/int | |
| name | string | |
| enrolled_at | timestamp | |
| gallery_embedding_count | int | grows over time |

### `face_gallery` (one-to-many with students)
| Field | Type | Notes |
|---|---|---|
| gallery_id | PK | |
| roll_no | FK | |
| embedding | vector(512) | |
| source_image_path | string | original crop used |
| added_via | enum | `enrollment` / `manual_label` / `low_conf_confirm` |
| added_at | timestamp | |

### `attendance_events` (evidence log — every match, every session)
| Field | Type | Notes |
|---|---|---|
| event_id | PK | |
| session_id | FK | |
| roll_no | FK, nullable | null until resolved for unrecognized entries |
| face_crop_path | string | **the actual captured image — this is what queries return** |
| full_frame_path | string | for spatial context |
| confidence_score | float | |
| match_type | enum | `auto` / `manual_label` / `low_conf_confirm` |
| captured_at | timestamp | |

### `review_queue`
| Field | Type | Notes |
|---|---|---|
| review_id | PK | |
| event_id | FK | links to attendance_events |
| status | enum | `pending` / `resolved` |
| resolved_roll_no | FK, nullable | |
| resolved_by | string | operator identity, for audit |
| resolved_at | timestamp | |

### `class_sessions`
| Field | Type | Notes |
|---|---|---|
| session_id | PK | |
| start_time / end_time | timestamp | 30-min window |
| class_id | FK | |

**Image storage**: store cropped face images and full frames on disk (or object storage — S3/GCS bucket for production) with paths referenced in the DB, not the raw bytes in the DB itself.

---

## 6. API Design (FastAPI recommended)

```
POST   /session/start                     → begin 30-min attendance window
POST   /session/{id}/capture              → ingest a new frame, run detection+recognition
GET    /session/{id}/review-queue         → list pending unrecognized faces
POST   /review/{review_id}/resolve        → { roll_no } → label + gallery update
GET    /session/{id}/query/{roll_no}      → returns status + evidence image + confidence
GET    /session/{id}/absentees            → final absentee roll list
POST   /students/enroll                   → formal enrollment (multi-image upload)
```

Each `/capture` call should be a background/async task so multiple frames across the 30-minute window don't block the UI.

---

## 7. UI/UX Requirements

1. **Live review panel**: shows unresolved faces as cards — cropped face large, full-frame thumbnail with bounding box below it, text input for roll number, submit button.
2. **Query panel**: operator types/selects a roll number → system displays the matched face crop, timestamp, and confidence, or an "Absent — not detected in any frame" message with the option to view all captured frames.
3. **Session dashboard**: live-updating count of present/unrecognized/absent as the 30-minute window progresses.
4. **Audit trail**: every manual label is logged with operator ID and timestamp (important for accountability if a mislabel happens).

---

## 8. Threshold Calibration & Evaluation

Before deployment:
1. Collect a calibration set from your actual classroom (lighting, camera angle, distance).
2. Sweep cosine similarity thresholds and plot **False Accept Rate vs. False Reject Rate** to choose τ_low and τ_high — do not use ArcFace's published benchmark thresholds blindly, since classroom conditions differ from benchmark datasets like LFW.
3. Track these production metrics post-deployment:
   - **Auto-match accuracy**: % of detections correctly matched without operator intervention.
   - **Review queue rate**: % of detections requiring manual labeling — should decrease over the semester as galleries grow.
   - **False present rate**: someone marked present who wasn't actually there (e.g., a look-alike mismatch) — the most important metric to keep near zero.
   - **Query evidence accuracy**: spot-check that returned images actually match the claimed roll number.

---

## 9. Privacy & Security Considerations

- Face embeddings and images are **biometric data** — handle under applicable data protection regulations (e.g., institutional policy, and law such as India's DPDP Act if deployed in India).
- Store images/embeddings with restricted access control; do not expose raw student photos via any public-facing endpoint.
- Define a **data retention policy** — e.g., purge session frame images after N days once attendance is finalized, retaining only the gallery embeddings needed for ongoing recognition.
- Obtain institutional/student consent for biometric enrollment before deployment — this is typically a hard requirement, not optional.
- Maintain the audit trail (Section 5, `resolved_by`) so any manual label can be traced back to an accountable operator.

---

## 10. Tech Stack Summary

| Layer | Choice |
|---|---|
| Detection + Recognition | `insightface` (RetinaFace + ArcFace, `buffalo_l`) |
| Vector Search | FAISS (`IndexIDMap` for incremental updates) |
| Backend/API | FastAPI |
| Database (structured) | PostgreSQL |
| Image storage | Local disk (prototype) → S3/GCS (production) |
| Frontend (review + query UI) | React (simple dashboard, or Streamlit for rapid prototyping) |
| Task queue (async frame processing) | Celery + Redis, or FastAPI `BackgroundTasks` for smaller scale |

---

## 11. Development Phases

1. **Phase 1 — Core recognition pipeline**: detection, embedding, FAISS matching, basic threshold logic. Validate on LFW + your own test photos.
2. **Phase 2 — Review queue + manual labeling**: unrecognized-face flagging, operator UI, gallery expansion logic, incremental FAISS updates.
3. **Phase 3 — Query/evidence module**: evidence image storage and retrieval, query API + UI.
4. **Phase 4 — Calibration & hardening**: threshold tuning on real classroom data, privacy/access controls, audit logging.
5. **Phase 5 — Hardware integration** *(future phase, out of current scope)*: camera trigger automation, edge deployment.

---

## 12. Whole-Classroom Group Photo Handling

This is a critical clarification worth stating explicitly: **the system never expects individual students to face the camera one at a time.** Every capture is a single wide shot of the entire room, and the detector must find and recognize *all* faces present in that one frame simultaneously. Implications for the design:

- **Camera requirement**: needs to be high enough resolution (minimum ~4K recommended for a mid-sized classroom, more for larger rooms) and positioned to cover the full seating area, since faces at the back of the room will occupy very few pixels compared to faces at the front.
- **Small-face detection**: RetinaFace and YOLOv8-face both support multi-scale detection, but very distant/small faces (<20–30px) will have unreliable embeddings even if detected. Two mitigations:
  - **Tiling**: split the full-resolution frame into overlapping tiles, run detection per tile, then merge/de-duplicate detections that appear in overlapping regions — this recovers small back-row faces that a single full-frame pass might miss.
  - **Super-resolution upscaling** on low-pixel-count face crops before embedding, if back-row recognition accuracy is too low in testing.
- **Occlusion**: in a packed classroom, students seated behind others will be partially blocked in any single frame. This is precisely why the design captures multiple frames across the 30-minute window (Section 2/6) rather than relying on one photo — a student occluded in frame 1 is very likely visible in frame 3 or 4 as people shift position.
- **Multi-camera option** (if one camera can't physically cover the whole room without excessive distortion at the edges): treat each camera as an independent frame source feeding into the same session's aggregation logic — a roll number is "seen" if matched in *any* camera's frame, at *any* timestamp, in the window.
- **Unrecognized-face queue at group-photo scale**: a single classroom photo can generate many unrecognized faces at once (e.g., 5–10 out of 60), not one. The review UI (Section 7) should support **batch review** — operator moves through a stack of flagged crops from that session efficiently, not a single pop-up per face.

---

## 13. Known Edge Cases

- **Duplicate labeling of the same unresolved face across frames**: if the same unrecognized student appears in multiple frames within one session, avoid creating redundant review entries — deduplicate by embedding similarity within the session before pushing to the queue.
- **Operator mislabeling**: since a wrong manual label pollutes that student's gallery going forward, consider a confirmation step or periodic gallery audit (e.g., flag gallery entries that are unusually dissimilar from the rest of that student's gallery).
- **New student mid-semester**: handled naturally — unrecognized face → operator enters a roll number not yet in `students` → system creates the record.
- **Look-alikes**: gallery-based matching with top-k averaging reduces but doesn't eliminate this risk; keep false-present rate monitored (Section 8).
