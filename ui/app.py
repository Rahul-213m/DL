"""
Attendance System — Tester UI
Guided workflow: Enroll → Start Session → Capture → Review → Results
"""
import base64
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
import streamlit as st

# ── Config ────────────────────────────────────────────────────────────────────
API = os.getenv("ATTENDANCE_API_URL", "http://localhost:8000")
ENV_FILE = Path(__file__).parent.parent / ".env"
HISTORY_FILE = Path(__file__).parent / "session_history.json"


def env_value(name: str, default: str) -> str:
    if name in os.environ:
        return os.environ[name]
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            key, separator, value = line.partition("=")
            if separator and key.strip() == name:
                return value.strip()
    return default

st.set_page_config(page_title="Attendance Tester", layout="wide", initial_sidebar_state="expanded")

# ── Session-state defaults ─────────────────────────────────────────────────────
for key, default in {
    "api_key": env_value("API_KEY", "changeme-dev-key"),
    "session_id": None,
    "reviews": [],
    "undo_stack": [],   # [{review_id, roll_no, ts}]
    "step": "enroll",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def headers():
    return {"X-API-Key": st.session_state.api_key}


def api(method, path, **kwargs):
    """Returns (ok: bool, data_or_error: any)."""
    try:
        r = getattr(requests, method)(f"{API}{path}", headers=headers(), timeout=120, **kwargs)
        try:
            body = r.json()
        except Exception:
            body = r.text
        if r.ok:
            return True, body
        detail = body.get("detail", body) if isinstance(body, dict) else body
        return False, _friendly(r.status_code, detail)
    except requests.exceptions.ConnectionError:
        return False, "Cannot reach the API — is the server running?"
    except Exception as exc:
        return False, str(exc)


def _friendly(status: int, detail) -> str:
    mapping = {
        409: "Already exists — no change needed.",
        404: "Not found.",
        413: "Image is too large (max 10 MB).",
        415: "Unsupported file type — use JPEG, PNG, or WebP.",
        422: str(detail),
        503: "Face recognition model is unavailable — check server logs.",
    }
    return mapping.get(status, f"Error {status}: {detail}")


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def img_b64(path: str) -> str | None:
    """Return base64 data-URI for a local image path, or None if missing."""
    if not path:
        return None
    p = Path(path)
    if not p.is_absolute():
        p = PROJECT_ROOT / p
    if p.exists():
        mime = "image/jpeg" if p.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
        return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"
    return None


# ── History helpers ────────────────────────────────────────────────────────────
def load_history() -> list:
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text())
        except Exception:
            return []
    return []


def save_history(records: list):
    HISTORY_FILE.write_text(json.dumps(records, indent=2, default=str))


def append_history(record: dict):
    records = load_history()
    records.append(record)
    save_history(records)


# ── .env read/write ────────────────────────────────────────────────────────────
def read_env() -> dict:
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    return env


def write_env_values(updates: dict):
    lines = ENV_FILE.read_text().splitlines() if ENV_FILE.exists() else []
    written = set()
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            k = stripped.split("=", 1)[0].strip()
            if k in updates:
                new_lines.append(f"{k}={updates[k]}")
                written.add(k)
                continue
        new_lines.append(line)
    for k, v in updates.items():
        if k not in written:
            new_lines.append(f"{k}={v}")
    ENV_FILE.write_text("\n".join(new_lines) + "\n")


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Connection")
    st.session_state.api_key = st.text_input(
        "API Key", value=st.session_state.api_key, type="password",
        help="Stored only in this browser session."
    )
    if st.button("Test connection"):
        ok, _ = api("get", "/health")
        st.success("Connected ✓") if ok else st.error("Connection failed")

    st.divider()
    st.header("🗺️ Workflow")

    session_ready = st.session_state.session_id is not None
    steps = [
        ("enroll",    "1 · Enroll",         False),
        ("session",   "2 · Start Session",  False),
        ("capture",   "3 · Capture",        not session_ready),
        ("review",    "4 · Review Queue",   not session_ready),
        ("results",   "5 · Results",        not session_ready),
    ]
    for key, label, disabled in steps:
        done = key == "enroll" or (session_ready and key != "session")
        icon = "✅" if done else "⏳"
        if st.button(f"{icon} {label}", disabled=disabled, width="stretch", key=f"nav_{key}"):
            st.session_state.step = key
            st.rerun()

    if session_ready:
        st.caption(f"Active session: **{st.session_state.session_id}**")

    st.divider()
    if st.button("🎚️ Threshold Playground", width="stretch"):
        st.session_state.step = "threshold"
        st.rerun()
    if st.button("📜 Session History", width="stretch"):
        st.session_state.step = "history"
        st.rerun()


# ── Main area ──────────────────────────────────────────────────────────────────
step = st.session_state.step

# ════════════════════════════════════════════════════════════════════════════════
# STEP 1 — ENROLL
# ════════════════════════════════════════════════════════════════════════════════
if step == "enroll":
    st.title("1 · Enroll Students")

    tab_folder, tab_manual, tab_manage = st.tabs(["📁 Folder Import", "📷 Manual Enroll", "🛠️ Manage & Repair"])

    with tab_folder:
        st.markdown(
            "Place **at least 8 single-face images** per student in `ENROLL_PHOTOS/<roll_no>/`, "
            "then click **Import**. New images are always added to the database; local folders are capped at 15 photos."
        )
        if st.button("▶ Import enrollment folders", type="primary"):
            with st.spinner("Importing…"):
                ok, data = api("post", "/students/import-folders")
            if ok:
                imported = data.get("imported", [])
                skipped = data.get("skipped", [])
                rows = [
                    {"Roll No": r["roll_no"], "Embeddings": r["gallery_embedding_count"],
                     "Status": "✅ Created" if r.get("status") == "created" else "✅ Updated"}
                    for r in imported
                ] + [
                    {"Roll No": r["roll_no"], "Embeddings": "—", "Status": f"⏭ {r['reason']}"}
                    for r in skipped
                ]
                if imported:
                    st.success(f"Imported or updated {len(imported)} student(s).")
                else:
                    st.info("No folders were imported or updated.")
                if rows:
                    st.table(rows)
            else:
                st.error(data)

    with tab_manual:
        with st.form("manual_enroll"):
            roll = st.text_input("Roll number")
            name = st.text_input("Name")
            images = st.file_uploader(
                "Upload 8–15 face photos", type=["jpg", "jpeg", "png", "webp"],
                accept_multiple_files=True
            )
            submitted = st.form_submit_button("Enroll", type="primary")
        if submitted:
            if not roll or not name:
                st.error("Roll number and name are required.")
            elif not 8 <= len(images) <= 15:
                st.error(f"Upload 8–15 images (you uploaded {len(images)}).")
            else:
                with st.spinner("Enrolling…"):
                    files = [("images", (f.name, f.read(), f.type)) for f in images]
                    ok, data = api("post", "/students/enroll",
                                   data={"roll_no": roll, "name": name}, files=files)
                if ok:
                    st.success(f"Enrolled **{roll}** with {data['gallery_embedding_count']} embeddings.")
                else:
                    st.error(data)

    with tab_manage:
        st.markdown(
            "See the face gallery stored for each student and whether the **database and the "
            "`ENROLL_PHOTOS/` folder agree**. No SQL knowledge required."
        )
        ok_st, students = api("get", "/students")
        if ok_st and students:
            st.dataframe(
                [{"Roll No": s["roll_no"], "Name": s["name"],
                  "Gallery embeddings": s["gallery_embedding_count"]} for s in students],
                width="stretch",
            )
        elif ok_st:
            st.info("No students enrolled yet.")
        else:
            st.error(students)

        st.divider()
        st.subheader("Consistency check")
        st.caption("Verifies that every student's embeddings and their ENROLL_PHOTOS folder line up.")
        if st.button("🔍 Run consistency check"):
            ok_c, report = api("get", "/system/consistency")
            if ok_c:
                if report.get("consistent"):
                    st.success("Database and enrollment folders are consistent.")
                else:
                    st.warning(f"{report['issue_count']} issue(s) found:")
                    st.table([{"Roll No": i["roll_no"], "Type": i["type"], "Detail": i["detail"]}
                              for i in report["issues"]])
            else:
                st.error(report)

        st.subheader("Repair")
        col_rep, col_reimp = st.columns(2)
        with col_rep:
            st.caption("Recompute every student's embedding count from the gallery and re-index FAISS.")
            if st.button("🧹 Repair counts & re-index"):
                ok_r, res = api("post", "/system/repair")
                if ok_r:
                    st.success(f"Repaired {res.get('repaired_count', 0)} student(s). Gallery index size: {res.get('gallery_size')}.")
                else:
                    st.error(res)
        with col_reimp:
            st.caption("Rebuild one student's gallery from the photos in ENROLL_PHOTOS/<roll_no>/.")
            reimp_roll = st.text_input("Roll number to re-import", key="reimp_roll")
            if st.button("♻️ Re-import this student"):
                if not reimp_roll.strip():
                    st.error("Enter a roll number.")
                else:
                    ok_i, res = api("post", f"/students/{reimp_roll.strip()}/reimport")
                    if ok_i:
                        st.success(f"Re-imported **{res['roll_no']}** with {res['gallery_embedding_count']} embeddings.")
                        if res.get("rejected_images"):
                            st.info(f"Skipped {len(res['rejected_images'])} image(s) with no usable face.")
                    else:
                        st.error(res)

# ════════════════════════════════════════════════════════════════════════════════
# STEP 2 — START SESSION
# ════════════════════════════════════════════════════════════════════════════════
elif step == "session":
    st.title("2 · Start Session")
    with st.form("start_session"):
        class_id = st.text_input("Class ID (e.g. CS101-A)", value="CS101")
        if st.form_submit_button("▶ Start Session", type="primary"):
            ok, data = api("post", "/session/start", json={"class_id": class_id})
            if ok:
                st.session_state.session_id = data["session_id"]
                st.session_state.reviews = []
                st.success(f"Session **{data['session_id']}** started for {class_id}.")
                st.session_state.step = "capture"
                st.rerun()
            else:
                st.error(data)

# ════════════════════════════════════════════════════════════════════════════════
# STEP 3 — CAPTURE
# ════════════════════════════════════════════════════════════════════════════════
elif step == "capture":
    sid = st.session_state.session_id
    st.title("3 · Capture Group Photo")
    st.caption(f"Session **{sid}**")

    frame = st.file_uploader("Upload group photo", type=["jpg", "jpeg", "png", "webp"])
    if frame and st.button("▶ Submit capture", type="primary"):
        with st.spinner("Submitting…"):
            ok, data = api("post", f"/session/{sid}/capture",
                           files={"frame": (frame.name, frame.read(), frame.type)})
        if ok:
            st.success("Frame accepted — processing in background.")
            st.info("Wait a moment, then check the review queue or session status.")
        else:
            st.error(data)

    st.divider()
    if st.button("🔄 Check session status"):
        ok, data = api("get", f"/session/{sid}/status")
        if ok:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Enrolled", data.get("enrolled", "—"))
            c2.metric("Present", data.get("present", "—"))
            c3.metric("Absent", data.get("absent", "—"))
            c4.metric("Pending review", data.get("pending", "—"))
        else:
            st.error(data)

# ════════════════════════════════════════════════════════════════════════════════
# STEP 4 — REVIEW QUEUE
# ════════════════════════════════════════════════════════════════════════════════
elif step == "review":
    sid = st.session_state.session_id
    st.title("4 · Review Queue")
    st.caption("Pending identity decisions stay visible until an operator resolves or dismisses them.")

    # Expire undo items older than 10 s
    now = time.time()
    st.session_state.undo_stack = [u for u in st.session_state.undo_stack if now - u["ts"] < 10]

    col_load, col_info = st.columns([1, 3])
    with col_load:
        show_all_sessions = st.checkbox(
            "Include earlier sessions",
            value=True,
            help="Shows unresolved reviews from all sessions, so no face is hidden after starting a new session.",
        )
        if st.button("🔄 Refresh reviews", type="primary"):
            st.session_state.reviews = []

    # Fetch on entry and every refresh/rerun rather than relying on a stale
    # session-state list. A capture is processed asynchronously, so this makes
    # newly-created review items appear as soon as the operator opens this step.
    queue_path = "/review-queue" if show_all_sessions else f"/session/{sid}/review-queue"
    ok, data = api("get", queue_path)
    if ok:
        st.session_state.reviews = data
    else:
        st.error(data)
    with col_info:
        n = len(st.session_state.reviews)
        if n:
            st.info(f"{n} face(s) awaiting review.")
        else:
            st.success("No pending reviews.")

    # Undo banners
    for undo_item in list(st.session_state.undo_stack):
        remaining = int(10 - (time.time() - undo_item["ts"]))
        cols = st.columns([7, 1])
        cols[0].warning(
            f"Resolved **#{undo_item['review_id']}** → `{undo_item['roll_no']}`. "
            f"Undo available for ~{remaining}s (original event preserved in audit log)."
        )
        if cols[1].button("↩ Undo", key=f"undo_{undo_item['review_id']}"):
            ok, data = api("post", f"/review/{undo_item['review_id']}/reopen")
            if ok:
                st.session_state.undo_stack = [
                    u for u in st.session_state.undo_stack
                    if u["review_id"] != undo_item["review_id"]
                ]
                st.info("Resolution undone. Reload the queue to re-review this face.")
                st.rerun()
            else:
                st.error(data)

    for review in st.session_state.reviews:
        rid = review["review_id"]
        score = review.get("confidence_score", 0.0)
        best_guess = review.get("best_guess") or ""
        score_icon = "🟢" if score >= 0.55 else ("🟡" if score >= 0.35 else "🔴")
        is_unknown = not best_guess
        review_title = (
            f"Could not identify this person — score {score:.3f}"
            if is_unknown
            else f"Is this {best_guess}? — score {score:.3f}"
        )

        with st.expander(
            f"{score_icon} Session {review.get('session_id', sid)} · Review #{rid} — {review_title}",
            expanded=True
        ):
            c_crop, c_frame, c_action = st.columns([1, 2, 2])

            with c_crop:
                st.caption("Detected face")
                uri = img_b64(review.get("face_crop_path", ""))
                st.image(uri) if uri else st.info("Crop not available")

            with c_frame:
                st.caption("Full frame context")
                uri2 = img_b64(review.get("boxed_frame_path", ""))
                st.image(uri2) if uri2 else st.info("Frame not available")

            with c_action:
                if is_unknown:
                    st.warning("I couldn't identify this person. Who is this person?")
                else:
                    st.info(
                        f"The model's best guess is **{best_guess}** at {score:.3f}. "
                        "Confirm it only if the face is actually that student; otherwise enter the correct person below."
                    )
                with st.form(f"resolve_{rid}"):
                    roll_input = st.text_input(
                        "Who is this person? Enter their roll number",
                        value=best_guess,
                        key=f"roll_{rid}",
                    )
                    name_input = st.text_input(
                        "Name (optional; used if this is a new student)",
                        key=f"name_{rid}",
                    )
                    operator = st.text_input("Your name / ID", value="operator", key=f"op_{rid}")
                    col_ok, col_skip = st.columns(2)
                    confirmed = col_ok.form_submit_button("✅ Save identity", type="primary")
                    skipped = col_skip.form_submit_button("❌ Not a match")

                if confirmed:
                    if not roll_input.strip():
                        st.error("Enter a roll number.")
                    else:
                        ok, data = api("post", f"/review/{rid}/resolve",
                                       json={"roll_no": roll_input.strip(), "name": name_input.strip() or None,
                                             "resolved_by": operator})
                        if ok:
                            st.session_state.undo_stack.append(
                                {"review_id": rid, "roll_no": roll_input.strip(), "ts": time.time()}
                            )
                            st.session_state.reviews = [
                                r for r in st.session_state.reviews if r["review_id"] != rid
                            ]
                            st.success(f"Marked as **{roll_input}**.")
                            st.rerun()
                        else:
                            st.error(data)

                if skipped:
                    ok, _ = api("post", f"/review/{rid}/dismiss")
                    if ok:
                        st.session_state.undo_stack.append(
                            {"review_id": rid, "roll_no": "Dismissed (Unidentified)", "ts": time.time()}
                        )
                        st.session_state.reviews = [
                            r for r in st.session_state.reviews if r["review_id"] != rid
                        ]
                        st.info("Face dismissed as unidentified/false detection.")
                        st.rerun()
                    else:
                        st.error(_)

# ════════════════════════════════════════════════════════════════════════════════
# STEP 5 — RESULTS / SESSION DASHBOARD
# ════════════════════════════════════════════════════════════════════════════════
elif step == "results":
    sid = st.session_state.session_id
    st.title("5 · Session Results")

    ok, status_data = api("get", f"/session/{sid}/status")
    if not ok:
        st.error(status_data)
        st.stop()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Enrolled", status_data.get("enrolled", "—"))
    c2.metric("Present", status_data.get("present", "—"))
    c3.metric("Absent", status_data.get("absent", "—"))
    c4.metric("Pending review", status_data.get("pending", "—"))

    ok2, ab = api("get", f"/session/{sid}/absentees")
    if ok2:
        ok3, all_students = api("get", "/students")
        enrolled_set = {s["roll_no"] for s in (all_students if ok3 else [])}
        absent_set = set(ab.get("absentees", []))
        present_set = enrolled_set - absent_set

        col_present, col_absent = st.columns(2)
        with col_present:
            st.subheader("✅ Present")
            for r in sorted(present_set):
                st.write(r)
        with col_absent:
            st.subheader("❌ Absent")
            for r in sorted(absent_set):
                st.write(r)

    st.divider()
    st.subheader("🔍 Visual Evidence Query")
    st.caption("Verify student attendance with the actual face image captured during this session.")
    q_col1, q_col2 = st.columns([3, 1])
    with q_col1:
        selected_roll = st.text_input("Enter Student Roll Number to Query", value=sorted(enrolled_set)[0] if (ok2 and enrolled_set) else "")
    with q_col2:
        st.write("")
        st.write("")
        check_evidence = st.button("Query Evidence", type="primary")

    if selected_roll and check_evidence:
        ok_q, res = api("get", f"/session/{sid}/query/{selected_roll.strip()}")
        if ok_q:
            if res.get("status") == "present":
                ev = res.get("evidence", {})
                st.success(f"Student **{selected_roll}** was marked **PRESENT** (Match: `{ev.get('match_type')}`, Confidence: `{ev.get('confidence_score', 0):.3f}`)")
                ec1, ec2 = st.columns(2)
                with ec1:
                    st.caption("Actual Face Captured in Class")
                    uri_face = img_b64(ev.get("face_crop_path"))
                    if uri_face:
                        st.image(uri_face, width=250)
                    else:
                        st.info("Face crop not available on disk")
                with ec2:
                    st.caption("Full Classroom Frame")
                    uri_frame = img_b64(ev.get("full_frame_path"))
                    if uri_frame:
                        st.image(uri_frame)
                    else:
                        st.info("Full frame not available on disk")
            elif res.get("status") == "pending":
                st.info(
                    f"Student **{selected_roll}** has an **unconfirmed** match awaiting review — "
                    "not yet counted as present. Resolve it in step 4."
                )
            else:
                st.warning(f"Student **{selected_roll}** is marked **ABSENT** — no matching face detected in this session.")
        else:
            st.error(res)

    st.divider()
    col_end, col_snap = st.columns(2)
    with col_end:
        if st.button("🔒 End Session", type="primary"):
            ok, data = api("post", f"/session/{sid}/end")
            if ok:
                env = read_env()
                append_history({
                    "session_id": sid,
                    "ended_at": datetime.now(timezone.utc).isoformat(),
                    "high_threshold": env.get("HIGH_CONFIDENCE_THRESHOLD", "?"),
                    "low_threshold": env.get("LOW_CONFIDENCE_THRESHOLD", "?"),
                    "enrolled": data.get("report", {}).get("summary", {}).get("enrolled"),
                    "present": data.get("report", {}).get("summary", {}).get("present"),
                    "absent": data.get("report", {}).get("summary", {}).get("absent"),
                    "notes": "",
                })
                st.success("Session ended and saved to history.")
                st.session_state.session_id = None
                st.session_state.step = "enroll"
                st.rerun()
            else:
                st.error(data)
    with col_snap:
        notes = st.text_input("Notes for history snapshot (optional)")
        if st.button("💾 Save snapshot"):
            env = read_env()
            append_history({
                "session_id": sid,
                "snapshot_at": datetime.now(timezone.utc).isoformat(),
                "high_threshold": env.get("HIGH_CONFIDENCE_THRESHOLD", "?"),
                "low_threshold": env.get("LOW_CONFIDENCE_THRESHOLD", "?"),
                "enrolled": status_data.get("enrolled"),
                "present": status_data.get("present"),
                "absent": status_data.get("absent"),
                "notes": notes,
            })
            st.success("Snapshot saved.")

# ════════════════════════════════════════════════════════════════════════════════
# THRESHOLD PLAYGROUND
# ════════════════════════════════════════════════════════════════════════════════
elif step == "threshold":
    st.title("🎚️ Threshold Playground")

    env = read_env()
    prod_high = float(env.get("HIGH_CONFIDENCE_THRESHOLD", 0.55))
    prod_low = float(env.get("LOW_CONFIDENCE_THRESHOLD", 0.35))

    st.markdown(f"**Current `.env` values** — HIGH: `{prod_high}` · LOW: `{prod_low}`")
    st.caption(
        "Adjust sliders to preview how existing capture scores would be re-bucketed. "
        "Click **Apply** to write new values to `.env` (API restart required to take effect)."
    )

    new_high = st.slider("HIGH_CONFIDENCE_THRESHOLD", 0.0, 1.0, prod_high, 0.01)
    new_low = st.slider("LOW_CONFIDENCE_THRESHOLD", 0.0, new_high, min(prod_low, new_high), 0.01)

    # Load scores from the active session if available
    sid = st.session_state.session_id
    scores = []
    if sid:
        ok, data = api("get", f"/session/{sid}/scores")
        if ok:
            scores = data

    if scores:
        auto_new = [s for s in scores if s["score"] >= new_high]
        review_new = [s for s in scores if new_low <= s["score"] < new_high]
        reject_new = [s for s in scores if s["score"] < new_low]

        auto_old = [s for s in scores if s["score"] >= prod_high]
        review_old = [s for s in scores if prod_low <= s["score"] < prod_high]
        reject_old = [s for s in scores if s["score"] < prod_low]

        c1, c2, c3 = st.columns(3)
        c1.metric("🟢 Auto-present", len(auto_new), delta=len(auto_new) - len(auto_old))
        c2.metric("🟡 Needs review", len(review_new), delta=len(review_new) - len(review_old))
        c3.metric("🔴 Rejected", len(reject_new), delta=len(reject_new) - len(reject_old))

        with st.expander("Score breakdown (all faces in session)"):
            for s in scores:
                bucket = "🟢 auto" if s["score"] >= new_high else ("🟡 review" if s["score"] >= new_low else "🔴 reject")
                st.write(f"{bucket} — `{s.get('roll_no') or 'unidentified'}` — {s['score']:.3f}")
    else:
        st.info("No capture scores available yet — run a capture first, then return here." if sid else
                "Start a session and run a capture to see live score data here.")

    st.divider()
    col_apply, col_cancel = st.columns(2)
    if col_apply.button("✅ Apply to .env", type="primary"):
        if new_low > new_high:
            st.error("LOW threshold cannot exceed HIGH threshold.")
        else:
            write_env_values({
                "HIGH_CONFIDENCE_THRESHOLD": str(new_high),
                "LOW_CONFIDENCE_THRESHOLD": str(new_low),
            })
            st.success(
                f"Written to `.env` (HIGH={new_high}, LOW={new_low}). "
                "Restart the API server for changes to take effect."
            )
    if col_cancel.button("← Back"):
        st.session_state.step = "enroll"
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# SESSION HISTORY
# ════════════════════════════════════════════════════════════════════════════════
elif step == "history":
    st.title("📜 Session / Test History")
    records = load_history()
    if not records:
        st.info("No history yet. Complete a session or save a snapshot from the Results page.")
    else:
        for rec in reversed(records):
            ts = (rec.get("ended_at") or rec.get("snapshot_at", "?"))[:19].replace("T", " ")
            sid = rec.get("session_id", "?")
            with st.expander(f"Session {sid} — {ts}", expanded=False):
                c1, c2, c3 = st.columns(3)
                c1.metric("Present", rec.get("present", "—"))
                c2.metric("Absent", rec.get("absent", "—"))
                c3.metric("Enrolled", rec.get("enrolled", "—"))
                st.caption(
                    f"HIGH={rec.get('high_threshold', '?')}  "
                    f"LOW={rec.get('low_threshold', '?')}"
                )
                if rec.get("notes"):
                    st.write(f"📝 {rec['notes']}")

        if st.button("🗑️ Clear history"):
            save_history([])
            st.success("History cleared.")
            st.rerun()

else:
    # Fallback — should not normally be reached
    st.session_state.step = "enroll"
    st.rerun()
