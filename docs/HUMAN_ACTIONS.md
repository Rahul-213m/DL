# HUMAN ACTIONS

**Everything here requires you. Nothing on this list is blocked on me.**

Ordered by priority. Each item says exactly what to run and what I need back.
Items marked **IRREVERSIBLE** or **NEEDS LAWYER** I will prepare but never run.

---

## 1. Buy the InsightFace commercial licence — or decide not to

**Blocks:** production accuracy. Not launch — the permissive baseline ships
today — but it caps recognition quality.

**Why:** the `buffalo_l` weights are explicitly "for non-commercial research
purposes only" (quoted in `docs/model_licensing.md`). This product is sold, so
they cannot ship.

**Upstream contact** (published by InsightFace, 2025-11-24):
`recognition-oss-pack@insightface.ai`

**Prepared draft — review and send:**

> Subject: Commercial licensing enquiry — pretrained face recognition pack
>
> Hello,
>
> We are building a commercial classroom-attendance product sold to colleges in
> India. Face images are processed in a self-hosted deployment; we do not resell
> or redistribute model weights.
>
> Your README states that the code is MIT but that "the training data containing
> the annotation (and the models trained with these data) are available for
> non-commercial research purposes only," and directs open-source face recognition
> packs such as `buffalo_l` to this address for licensing.
>
> Could you please advise on:
>
> 1. Commercial licensing terms for the `buffalo_l` pack (SCRFD detector and
>    ArcFace recogniser), including whether a hosted-SaaS deployment is covered
>    and whether redistribution of weights is permitted.
> 2. Pricing structure — per seat, per room, per recognition, or a flat annual
>    licence.
> 3. Whether the licence extends to future model updates, and to any pack you
>    would recommend as your current best-accuracy option.
> 4. Whether an on-premise/air-gapped deployment is supported, since some
>    colleges will require it.
> 5. Any attribution or reporting obligations we would owe.
>
> For context on scale: approximately 300 students per classroom, 3 scans per
> teaching day, deployed at roughly 20–50 institutions.
>
> We are currently shipping with the OpenCV YuNet + SFace baseline (MIT and
> Apache-2.0 respectively) and treat this as a quality upgrade rather than a
> blocker, so there is no urgency on your side — but we would like to understand
> the option.
>
> Thank you.

**Then record the licence** (no code change needed):

```bash
mkdir -p /etc/attendance
cat > /etc/attendance/models.json <<'JSON'
{
  "models": {
    "licensed_placeholder": {
      "version": "<version from contract>",
      "license": {
        "license_name": "commercial-licensed",
        "commercial_use": true,
        "training_data": "<as stated in contract>",
        "source_url": "contract://<your reference>",
        "sha256": "<sha256sum of the supplied weights>",
        "legal_review_required": false
      }
    }
  }
}
JSON
```

**Cost to ask for — ESTIMATE, do not budget from this:** if licensing is priced
per recognition, our volume is ~2,400 faces per room-scan × 750 scans/room/year.
Ask for per-room and flat-annual pricing, which is what would make the numbers
work.

---

## 2. **NEEDS LAWYER** — SFace training-data provenance

**Blocks:** commercial launch (not a code block).

SFace is Apache-2.0 for the *released files*, but **the publisher never states
which images trained the network**. Apache-2.0 grants nothing about the training
corpus. If that corpus contains scraped photographs of identifiable people, a
commercial deployment may carry obligations.

This is currently an **advisory, not a startup blocker** — deliberately, because
SFace is the only commercially usable embedder available today and blocking it
would make the product unshippable. That trade is pinned by
`test_outstanding_legal_review_does_not_block_startup` so nobody changes it
without noticing.

**Questions for counsel:**
1. Does deploying Apache-2.0-licensed model *weights* of undocumented provenance
   to paying customers create liability?
2. Does it differ for on-prem (we hold the data) versus SaaS (we also hold it)?
3. Does DPDP Act 2023 impose anything on the *provenance* of biometric models?
4. Would a written representation from OpenCV help, or do we need our own audit?

**Cheaper mitigation available:** option 3 in `docs/model_licensing.md` — train
our own on consented data. Slow, but it retires this question permanently.

---

## 3. **IRREVERSIBLE** — purge biometric data and the secret from git history

**Do not run this until you have confirmed the backup is good.** I have NOT run
it. `.git` is 919 MB and still contains 535 face images, 850 MB of crops, a
`DL_PROJECT.zip`, a `dl.zip`, and the `.env` API key.

### Step 1 — back up first

```bash
cd ~/Documents
cp -a DL_PROJECT DL_PROJECT.backup-$(date +%Y%m%d)
du -sh DL_PROJECT.backup-*
```

Confirm `DL_PROJECT.backup-*/data` and `.../ENROLL_PHOTOS` have the same file
counts as the live tree (496 and 39 respectively).

### Step 2 — install the tool

```bash
pip install git-filter-repo
```

### Step 3 — purge (this rewrites history)

```bash
cd ~/Documents/DL_PROJECT

git filter-repo \
  --path .env \
  --path data \
  --path ENROLL_PHOTOS \
  --path-glob '*.zip' \
  --path ui/session_history.json \
  --path-glob '*__pycache__*' \
  --invert-paths \
  --force
```

### Step 4 — verify

```bash
git log --oneline | wc -l                 # commits are preserved, not dropped
git ls-files | grep -cE 'data/|ENROLL_PHOTOS|\.env$|\.zip$'   # must print 0
du -sh .git                               # should be far smaller than 919M
git fsck --no-progress                     # repository must still be sound
```

### Step 5 — every clone must be discarded, then force-push

```bash
# Local
rm -rf ~/Documents/DL_PROJECT/.venv

# Remote (IRREVERSIBLE — rewrites shared history)
git remote set-url origin <YOUR-NEW-EMPTY-REPO>
git push -u origin feature/industrial-hardening
git push origin main
```

> ⚠️ After Step 5 the old remote still holds the data until garbage-collected.
> **Contact GitHub to purge it**, or delete and recreate the repository.

### Also: rotate the exposed key

The `changeme-dev-key` was committed in plaintext. It is a published default so
it is already compromised, but if you ever set a real one:

```bash
python scripts/generate_secrets.py          # new API_KEY + JWT_SECRET
# update your deployment secret store
```

---

## 4. Tell me whether the existing data is real

I could not determine this, and it changes the compliance obligation:

```bash
cd ~/Documents/DL_PROJECT
sqlite3 attendance.db "select roll_no, name, enrolled_at from students;"
sqlite3 attendance.db "select class_id, start_time from class_sessions;"
sqlite3 attendance.db "select resolved_by, count(*) from review_queue group by 1;"
ls ENROLL_PHOTOS/*/ | head
```

The 4 students are named `R1`–`R4` (roll number as name), which looks like
test data. **But the photos are real photographs of real people.** If any
enrolled face is an identifiable person who did not consent, that is a DPDP Act
2023 issue independent of where the files live.

**Tell me: real students, or test data? If real, is consent documented?**

Also confirm your backup path — you said you backed the project up but did not
give the location, and Step 1 above needs a known-good copy.

---

## 5. Hardware: I cannot test any of this

**Everything in W5 runs in simulation.** The following need your hardware.

### 5a. Confirm the servo — I need this to finish W5

The brief left the model as a placeholder. **What servo and driver board do you
actually have?**

MG996R and similar hobby servos are a real concern: they have no position
feedback, so the software cannot detect a stall and cannot know its true angle.
They also buzz and heat under continuous load. If that is what you have, the
`hardware/wiring.md` guide will recommend replacing it.

**Please answer:** servo model? driver board? Is there any position feedback, or
is it open-loop step counting?

### 5b. Confirm the phone

Which phone, and which capture app? **IP Webcam, DroidCam, `adb`, or something
else?** The client is written against IP Webcam's HTTP API by default and needs
adjusting if you use something else.

Also: **do you have the phone and servo at all right now, or are they still to be
bought?** If not bought yet, read `docs/hardware/bom.md` first — the answer may
change what you buy.

### 5c. Classroom geometry

I need real numbers for the pixels-per-face calculation:

```
room width (m)  x  room depth (m)  x  camera mount height (m)
number of student seats, and how they are arranged (rows x columns?)
typical distance from camera to back row (m)
```

**Do the maths yourself, with numbers, before you buy anything** — see
`docs/hardware/pixels_per_face.md`. The short version: whether one phone on a
hobby pan can resolve back-row faces is a question of geometry, not of model
quality, and no amount of model work fixes it if the answer is no.

### 5d. Wiring and calibration

Once W5 lands, you will need to:

1. Assemble and wire the edge computer + servo driver (see `hardware/wiring.md`).
2. Run the homing/calibration routine and record the classroom calibration file.
3. Physically verify the angle limits do not hit the wall.

---

## 6. AWS: benchmark on a GPU, then `terraform apply`

**I wrote the Terraform and validated it. I have NOT applied it — it would
create billable resources.**

### Step 1 — create the benchmark instance

```bash
# In AWS console or via your existing setup:
#   Instance type: g4dn.xlarge  (NVIDIA T4, 16 GB)
#   AMI: Ubuntu 24.04
#   Storage: 100 GB gp3
#   Region: your choice
```

### Step 2 — run the benchmark on it

```bash
git clone <your-repo> ~/attendance && cd ~/attendance
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

cp .env.example .env
sed -i 's/^ONNX_PROVIDERS=.*/ONNX_PROVIDERS=TensorrtExecutionProvider,CUDAExecutionProvider,CPUExecutionProvider/' .env
sed -i 's/^INFERENCE_BATCH_SIZE=.*/INFERENCE_BATCH_SIZE=32/' .env

# CPU baseline first, on the same box, so the comparison is apples-to-apples
ONNX_PROVIDERS=CPUExecutionProvider python scripts/benchmark_backends.py --full

# Then GPU
python scripts/benchmark_backends.py --full

python scripts/benchmark_pipeline.py --students 300 --frames 8
```

**What I need back:** the printed table. It fills in the GPU rows in
`docs/benchmarks.md`, which are currently labelled `UNVERIFIED`.

> I will not claim a GPU speedup until you paste real numbers here.

### Step 3 — Terraform (only after the benchmark satisfies you)

```bash
cd infra/terraform

terraform init
terraform validate          # I ran this; it passes
terraform plan -out=tfplan  # READ THE PLAN. Nothing is applied by me.
terraform show tfplan

# Apply only when you have read the plan and approved the monthly cost:
terraform apply tfplan
```

**Cost control:** the plan includes a `g4dn.xlarge` GPU worker. That is the
single most expensive item. `infra/terraform/README.md` gives the estimate and
how to destroy everything.

---

## 7. Real classroom data — for the acceptance criteria

**No evaluation set exists.** `attendance.db` has 32 attendance events for 4
students. There is nothing to measure TAR@FAR on.

Protocol is in `docs/data_collection_protocol.md`. Short version:

1. Get consent in writing from the students (template in the same doc).
2. Capture ≥ 3 full-classroom photos per condition, at 3 lighting conditions,
   across ≥ 3 different rooms, with a ground-truth roster.
3. Run `python scripts/evaluate.py --dataset <path>`.
4. The numbers that come out replace every `UNVERIFIED` in `docs/benchmarks.md`.

**Until you do this, no accuracy claim in the documentation is verified.**
I will keep labelling them UNVERIFIED rather than inventing them.

---

## 8. Product decisions I need

| Question | Why it matters | Default I will assume |
|---|---|---|
| First customer / pilot college? | Shapes the deployment target and the timetable feature | One college, one building, ~20 rooms |
| Do teachers need individual logins, or one shared console per room? | Determines the auth build | Individual logins (admin/teacher/readonly) |
| SMS/WhatsApp notification of absent students? | Changes the attendance service | Not built; API webhook only |
| Is the deployment on-prem per college, or our cloud? | Decides multi-tenant vs single-tenant | Multi-tenant cloud, on-prem edge |
| Must it work fully offline (air-gapped college)? | Decides edge/cloud sync architecture | No; edge queues offline and syncs later |

---

## 9. Ongoing housekeeping

| When | Command |
|---|---|
| Daily (cron) | `python -m app.cli purge --apply` |
| After a model update | `python scripts/verify_model_hashes.py` |
| Before every release | `python -m app.cli doctor` |
| Quarterly | Review `docs/model_licensing.md` for licence changes |

---

## Priority order

1. **#3 purge git history** — active privacy exposure, cheap to fix, the clock is running.
2. **#4 tell me if the data is real** — determines whether we have a compliance incident.
3. **#1 InsightFace licence** — long lead time, no rush, but start the conversation.
4. **#5b/#5c hardware answers** — W5 is in simulation until these land.
5. **#6 AWS GPU benchmark** — unblocks every performance claim.
6. **#7 real classroom data** — unblocks every accuracy claim.
7. **#2 lawyer** — before commercial launch, not before pilot.
8. **#8 product decisions** — needed by W6/W7, defaults will hold until then.


---

## Added during W5: the hardware decision this software forces

### 5d. THE CAMERA NEEDS A MOTORISED OPTICAL TELEPHOTO

Not a preference. At 70 deg FOV and 4608 px, a phone produces about 62 px of
face at 8 m; recognition needs 80 px. The back of a lecture hall is below the
floor at 1x, and **digital zoom does not fix it**.

Confirm before ordering:

- [ ] Does the candidate lens have a **motorised optical** telephoto
      (roughly 3x or 4x), or only digital zoom? Digital is worth nothing here.
- [ ] Is the main camera wide enough NOT to be the ultra-wide? A 120 deg FOV
      gives 17 px at 12 m: undetectable.
- [ ] What is the **exact horizontal FOV of the still**, not the equivalent
      35 mm figure? The model needs the real number.
- [ ] Can focus be **locked** after focusing? An AF search blurs the first
      frames of every sweep.

Then, on the real device, in the real room: seat one person at the back row,
capture a still, measure face width in pixels, and compare against
`docs/hardware/pixels_per_face.md`. **Replace the model's numbers with the
measurement** in both that document and `SimulatedCamera`.

### 5e. The camera's actual control interface

`IpWebcamDriver` assumes the Android "IP Webcam" app and is **unverified**.
Confirm which app (if any) the operator uses, and whether it exposes:

- [ ] A full-resolution still endpoint (not just a video stream)
- [ ] A zoom command, and whether it is optical or digital
- [ ] A focus lock
- [ ] An exposure lock

If the app cannot lock exposure, the same student is captured at different
brightness in different angles, which degrades embedding consistency. If
nothing can be locked, that is a hardware finding, not a software problem.
