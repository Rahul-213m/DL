# Benchmarks

Every number on this page is labelled. The labels are not decoration:

| Label | Meaning |
|---|---|
| **MEASURED** | Run on this machine, on real images, with the command shown. |
| **ESTIMATE** | Computed from a stated formula and stated assumptions. |
| **SYNTHETIC** | Generated data. Proves the code path, never real-world accuracy. |
| **UNVERIFIED** | Not yet measured. The protocol to measure it is given. |

**Measurement machine** (all MEASURED figures below, unless stated):
Ubuntu 24.04.5 LTS, Python 3.13.11, x86_64, **integrated graphics only, no GPU**,
ONNX Runtime `CPUExecutionProvider`, OpenCV 5.0.0, YuNet 2023mar, SFace 2021dec.
Date: **2026-09-29**.

> ⚠️ **No GPU number appears anywhere in this document.** The dev machine has no
> GPU. Every GPU figure is UNVERIFIED with a protocol in §6. I will not quote a
> speedup I have not observed.

---

## 1. The channel-order defect (audit 4.1) — MEASURED

**Command:**
```bash
python scripts/measure_channel_order.py --photos ENROLL_PHOTOS --per-student 8
```

**Method:** paired. The same 23 decoded images (4 students) are embedded under
both channel orders, so the pair populations are identical and a difference
cannot be manufactured by different images surviving.

| Metric | RGB (legacy, wrong) | BGR (fixed) | Delta |
|---|---|---|---|
| students / photos | 4 / 23 | 4 / 23 | — |
| same-person pairs | 71 | 71 | — |
| different-person pairs | 182 | 182 | — |
| same-person mean | 0.4721 | **0.6475** | +0.175 |
| same-person p05 | 0.1210 | **0.4036** | +0.283 |
| different-person mean | 0.1829 | 0.2218 | +0.039 |
| different-person p95 | 0.2606 | 0.2513 | −0.009 |
| **separability** (same − diff) | **+0.2893** | **+0.3679** | **+0.079** |
| intra-student spread (lower better) | 0.5663 | **0.4628** | −0.104 |

**Reading.** BGR raises separability by **+0.079 (+27% relative)** and, more
importantly, lifts the 5th percentile of same-person similarity from 0.121 to
0.404. That p05 is the number that matters: it is the worst-case same-person
match, and at 0.121 the legacy space was so unstable that a low threshold would
have been required, which in turn invites false accepts.

**Honest caveat.** Because the legacy pipeline used RGB *consistently* for both
enrollment and inference, matching still largely worked. The damage is (a)
absolute embedding quality and (b) that thresholds calibrated on the RGB space
are not comparable to any published ArcFace or SFace figure.

---

## 2. Detector operating point — MEASURED

**Command:**
```bash
python scripts/sweep_detector.py --limit 24
```

**Data:** 24 single-person portraits, 3060×4080. Label: the one large centred
face is a true positive; every other detection is a false positive.

| working size | threshold | FP/img | recall | precision | ms/img |
|---|---|---|---|---|---|
| **320** | **0.70** | **0.17** | 0.75 | 0.64 | **25.9** |
| 320 | 0.60 | 0.25 | 0.75 | 0.60 | 26.3 |
| 320 | 0.90 | 0.00 | 0.58 | 0.70 | 26.8 |
| 480 | 0.70 | 0.50 | 0.75 | 0.50 | 30.9 |
| 640 | 0.70 | 0.79 | 0.75 | 0.42 | 46.0 |
| 960 | 0.70 | 1.00 | 0.75 | 0.38 | 87.5 |
| 1280 | 0.60 | **1.58** | 0.75 | 0.29 | **153.1** |
| 1280 | 0.70 | 1.08 | 0.71 | 0.34 | 151.1 |

### The single most important result

Running YuNet at full 12 MP resolution costs **6× the latency and 9× the false
positives** for **zero recall gain**. `DETECTOR_WORKING_SIZE=320` is therefore
the default, and this is why: the model is fully convolutional and was designed
for a ~320 px input. The earlier code called `setInputSize((width, height))`,
which silently overrode the configured working size — a bug found by
measurement, not by reading, and now pinned by
`test_working_size_is_not_ignored`.

### Honest limitations of this table

- **Recall caps at 0.75** and does not improve with working size. 6 of 24
  portraits found no face at all. Cause **not yet diagnosed** — most likely
  extreme pose or blur, but that is a hypothesis, not a finding. Tracked in
  `docs/LIMITATIONS.md`.
- **This is portrait recall, not classroom recall.** The question that actually
  matters — do back-row faces get detected — is **UNVERIFIED** until a labelled
  classroom set exists. See §5.
- `ms/img` is CPU on a laptop. It is **not** the production number.

---

## 3. Per-frame latency — MEASURED (CPU, 4K)

**Command:** `python -m pytest tests/test_w2_perception.py -q` plus a direct run
over `dummy_test/*.jpg`, each 4608×3456 (12 MP).

| Stage | Time | Share |
|---|---|---|
| `decode_ms` (PNG/JPEG → BGR array) | **320–345** | **~46%** |
| `detect_ms` (YuNet, 10 tiles at 4K) | 345–382 | ~50% |
| `quality_align_embed_ms` | 20–147 | ~2% |
| **total per 4K frame** | **694–1021** | 100% |

**The finding that matters: this is dominated by decode and detect, not by
embedding.** Face *recognition* was never going to be the bottleneck in a
classroom; *locating* faces is. That reframes where optimisation effort belongs
and is why the scan planner (fewer, better-targeted frames) buys more than a
faster embedder would.

**UNVERIFIED:** end-to-end scan time for a full sweep (8 angles × wide pass +
zoom passes), GPU acceleration, and behaviour at 300 faces per frame. §6 has
the protocol.

---

## 4. Tiling geometry — MEASURED (arithmetic, verified by test)

| Frame | Grid | Detector passes |
|---|---|---|
| 4608 × 3456 (12 MP classroom) | 3 × 3 + full frame | **10** |
| 6000 × 4500 (27 MP, under the 36 MP guard) | 4 × 3 + full frame | 13 |
| 6000 × 4500 with `max_tiles=16` | — | 16 (capped) |
| 640 × 480 (small frame) | no tiling | **1** |

Pinned by `test_four_k_frame_tile_count_is_documented` and
`test_no_tiling_for_a_small_frame`. The last row caught a real regression:
the new pipeline tiled unconditionally and doubled the detector work on every
small frame.

---

## 5. Recognition accuracy — UNVERIFIED (no evaluation data exists)

**There is no evaluation set.** The live database has 32 attendance events for
4 students. There is nothing to compute TAR@FAR on, so every recognition
figure the brief asks for is **UNVERIFIED**.

| Metric | Status | Why |
|---|---|---|
| TAR @ FAR = 0.1% | **UNVERIFIED** | Needs a labelled held-out set. |
| FAR / FRR | **UNVERIFIED** | Same. |
| Coverage % of seated students | **UNVERIFIED** | Needs a roster + a classroom photo. |
| Duplicate rate | **UNVERIFIED** | Needs ground-truth identities per frame. |
| Unknown rate trend | **UNVERIFIED** | Needs a multi-session pilot. |
| End-to-end scan time | **UNVERIFIED** | Needs the full scan planner (W5). |

**Protocol:** `docs/data_collection_protocol.md`. Until it is run, no
accuracy claim in any document is verified, and this repository will keep saying
so.

### 5.1 The decision rules, stated honestly

Even without measured data, the *shape* of the safety argument is known:

- **Margin rule.** A candidate is auto-confirmed only if it beats the runner-up
  by `MATCH_MARGIN_THRESHOLD` (0.08). The project's own history records a real
  0.632-vs-0.631 R1→R3 false positive; that pair is now UNCERTAIN, not a
  false "present". Tested in
  `test_margin_rule_fires_above_the_high_threshold`.
- **Quality gate.** A poor face can be matched but can never auto-confirm
  attendance. Tested in `test_small_but_usable_face_is_poor_not_rejected`.
- **Roster prior.** A high score on someone not enrolled in the class is
  UNCERTAIN, never auto-present.
- **Presence rule.** "Seen at least once from at least N distinct angles" is
  configurable, because a single lucky close-up is the most common real false
  accept.

**What these do NOT give:** they cannot separate two students whose embeddings
are genuinely too close at any threshold. That pair goes to the human queue
forever. The correct response is to measure the per-pair confusion matrix and
surface the worst offenders, not to tune until the average looks good.

---

## 6. GPU benchmark protocol — UNVERIFIED until run

**On an AWS `g4dn.xlarge` (NVIDIA T4, 16 GB), Ubuntu 24.04:**

```bash
git clone <repo> ~/attendance && cd ~/attendance
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env

# 1. CPU baseline ON THE SAME BOX, so the comparison is apples-to-apples
ONNX_PROVIDERS=CPUExecutionProvider python scripts/benchmark_backends.py --full

# 2. Then CUDA
ONNX_PROVIDERS=TensorrtExecutionProvider,CUDAExecutionProvider,CPUExecutionProvider \
  python scripts/benchmark_backends.py --full

# 3. Then pipeline throughput at classroom scale
python scripts/benchmark_pipeline.py --students 300 --frames 8
```

**Paste the output back** and I will fill in the GPU rows here. Until then they
stay UNVERIFIED. Full instructions: `docs/HUMAN_ACTIONS.md` item 6.

---

## 7. Backend comparison — the accuracy question that matters

`scripts/benchmark_backends.py` compares YuNet+SFace (permissive, shippable)
against SCRFD+ArcFace (`buffalo_l`, non-commercial, dev only) on YOUR images,
reporting TAR@FAR, per-distance and per-pose breakdown.

**The privacy/licensing constraint is the reason this section is empty rather
than a table.** `buffalo_l` is the accuracy reference and cannot ship. Running
the comparison tells us how much the permissive baseline gives up, and that
number is a commercial input, not a code decision.

**Design note.** The identity engine is built to compensate as far as honestly
possible (margin rule, multi-exemplar prototypes, roster priors, cross-frame
consensus, required-distinct-angles), and `docs/model_licensing.md` §3 lists
exactly what each compensation buys and — importantly — what it **cannot** buy.
The honest residual is: if SFace cannot separate two particular students at any
threshold, no decision-layer engineering recovers it.

---

## 8. Cost per room — ESTIMATE

Formula and AWS prices are in `docs/model_licensing.md` §3 (option 4), fetched
2026-09-29. Summary: AWS Rekognition is **~$12.54 per room per year** of API
cost, which is *not* a reason to prefer self-hosting. Privacy sovereignty is.
The full infrastructure cost model, including EC2/RDS/S3, is in
`docs/cost_model.md` (W11).

> **Correction on record.** An earlier draft of `docs/model_licensing.md` quoted
> "$0.0025 per face" and computed ~$4,500/room/year. That figure was recalled,
> not fetched. The published price is **per image** ($0.0010 for Group 1 and
> Group 2 in the first million). The corrected figure is ~$12.54/room/year.
