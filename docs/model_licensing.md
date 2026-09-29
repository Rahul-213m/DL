# Model Licensing

**Status: PRODUCTION BLOCKER — partially resolved.**

**Last verified: 2026-09-29** against upstream sources by fetching them, not by
recalling them. Verification commands are in
[HUMAN_ACTIONS.md](HUMAN_ACTIONS.md) item 1.

---

## 1. The problem in one paragraph

A face-recognition product is two things stacked: **code** and **weights**. They
are licensed separately, and for the model most people reach for first
(InsightFace) the split is favourable for research and fatal for a product. We
cannot ship the current system commercially until this is resolved. Everything
else in this repository is built so that swapping the model is a configuration
change, not a rewrite.

## 2. Verified licence text

### 2.1 InsightFace — the code is MIT, the weights are not

Fetched from <https://github.com/deepinsight/insightface> on 2026-09-29. The
project's own README states:

> **License**
>
> The code of InsightFace is released under the MIT License. There is no
> limitation for both academic and commercial usage.
>
> **The training data containing the annotation (and the models trained with
> these data) are available for non-commercial research purposes only.**
>
> Both manual-downloading models from our github repo and auto-downloading
> models with our python-library follow the above license policy (which is for
> non-commercial research purposes only).

And, dated 2025-11-24:

> For open-sourced face recognition models (e.g., buffalo_l package), please
> contact **recognition-oss-pack@insightface.ai** for licensing.

Verified mechanically:

| Fact | How verified | Result |
|---|---|---|
| Weights origin | `insightface/utils/storage.py:5` | `BASE_REPO_URL = 'https://github.com/deepinsight/insightface/releases/download/v0.7'` |
| So auto-download fetches weights, not code | `download()` builds `%s/%s.zip % (BASE_REPO_URL, name)` | Confirmed — `pip install insightface` silently downloads NC weights |
| Installed version | `pip show insightface` | `1.0.1` |
| PyPI metadata declares no licence | `importlib.metadata` | `License: None` — **do not rely on package metadata to decide licensing** |

**Conclusion:** the Python package being MIT does **not** make `buffalo_l`
usable commercially. The weights are the trained artefact and they are
explicitly non-commercial.

Recorded weight hashes (MEASURED 2026-09-29, `sha256sum`):

| File | SHA-256 | Role |
|---|---|---|
| `det_10g.onnx` | `5838f7fe053675b1c7a08b633df49e7af5495cee0493c7dcf6697200b85b5b91` | SCRFD detector |
| `w600k_r50.onnx` | `4c06341c33c2ca1f86781dab0e829f88ad5b64be9fba56e56bc9ebdefc619e43` | ArcFace R50 embedder |
| `2d106det.onnx` | `f001b856447c413801ef5c42091ed0cd516fcd21f2d6b79635b1e733a7109dbf` | alternative detector |
| `1k3d68.onnx` | `df5c06b8a0c12e422b2ed8947b8869faa4105387f199c477af038aa01f9a45cc` | landmark model |
| `genderage.onnx` | `4fde69b1c810857b88c64a335084f1c3fe8f01246c9a191b48c7bb756d6652fb` | gender/age |
| `buffalo_l.zip` | `80ffe37d8a5940d59a7384c201a2a38d4741f2f3c51eef46ebb28218a7b0ca2f` | release archive |

### 2.2 OpenCV Zoo — permissive files, and one open question

Fetched from `opencv/opencv_zoo` model READMEs on 2026-09-29.

**YuNet (detector)** — `models/face_detection_yunet/README.md`:

> All files in this directory are licensed under [MIT License].

Publisher-reported WIDER Face validation: AP_easy 0.834 / AP_medium 0.824 /
AP_hard 0.708. Model source is `ShiqiYu/libfacedetection.train`, a research
release — consistent with the MIT grant. Documented to detect faces "between
around 10x10 to 300x300", which is excellent for the back-row problem.

SHA-256 (MEASURED 2026-09-29): `8f2383e4dd3cfbb4553ea8718107fc0423210dc964f9f4280604804ed2552fa4`

**SFace (recogniser)** — `models/face_recognition_sface/README.md`:

> All files in this directory are licensed under [Apache 2.0 License].

Architecture: MobileFaceNet trained with the SFace loss (arXiv:2205.12010).
Publisher-reported accuracy 0.9940 on opencv_zoo `tools/eval`.

SHA-256 (MEASURED 2026-09-29): `0ba9fbfa01b5270c96627c4ef784da859931e02f04419c829e83484087c34e79`

> ⚠️ **NEEDS LAWYER.** Apache-2.0 grants rights in **the released files**. It
> says nothing about **which images trained the network**. The publisher does
> not document SFace's training corpus. If that corpus contains scraped
> photographs of identifiable people, a downstream commercial deployment may
> carry obligations regardless of the code licence. This is a genuine open
> question, not a formality, and it is tracked as HUMAN_ACTIONS item 2.
>
> Our engineering position: this is an **advisory, not a blocker** — see §5.

## 3. Options

| # | Option | Accuracy | Cost | Legal risk | Effort | Verdict |
|---|---|---|---|---|---|---|
| **1** | **Buy the InsightFace commercial licence** | Best available | Per-seat / annual fee, **NEEDS LAWYER + purchase** | Low once signed | Low (config change) | **Recommended primary** |
| **2** | Ship YuNet + SFace now | Materially lower, **UNVERIFIED pending our benchmark** | $0 | Medium (SFace provenance) | **Done** | **Recommended launch baseline** |
| **3** | Train our own on consented data | Unknown until trained | GPU hours + labelling | Low, but slowest | High (months) | Medium-term differentiator |
| **4** | AWS Rekognition (managed) | Strong, vendor-managed | **Per-image, see §4** | Data leaves our tenancy | Low | Fallback for pilots |

### Option 1 — Buy the InsightFace commercial licence

The contact is published upstream. Everything else is a commercial negotiation:
scope, seats, redistribution inside a hosted SaaS, and whether the licence
extends to model updates. A prepared email draft is in
[HUMAN_ACTIONS.md](HUMAN_ACTIONS.md) item 1.

**This is the only option that keeps the accuracy we already measured.** It
should be pursued in parallel with shipping option 2, not instead of it.

### Option 2 — Ship the permissive baseline (already implemented)

`DETECTOR_BACKEND=opencv_yunet` + `EMBEDDER_BACKEND=opencv_sface`. Both are
registered with `commercial_use=true`, so the production guard permits them and
the product can start today.

**What this costs, stated honestly.** SFace is 128-d; ArcFace is 512-d. That is
a quarter of the representational capacity. YuNet is also a much weaker
detector than SCRFD on dense, small, partially occluded faces, which is exactly
the classroom case. We will measure the actual gap with
`scripts/benchmark_backends.py` (see `docs/benchmarks.md`) before quoting any
number. **Do not assume it is small.**

**What the identity engine does to compensate** (each is implemented and
tested in W6):

| Compensation | What it buys | What it cannot buy |
|---|---|---|
| Margin rule on k=2 search | Kills the ambiguous top-1 class of errors, which is where the SFace-vs-ArcFace gap bites hardest | Cannot create information the embedding does not contain |
| Multi-exemplar prototypes (up to N per student) | Recovers within-class variance SFace is more sensitive to | Bounded by gallery size; cannot fix a systematically wrong embedding |
| Roster + seat priors | Large recall win in practice: if the class is R1–R60 and the top-3 are all in range, a wrong-but-in-roster guess becomes a *ranked question* for the operator | Requires a seat map and a roster, i.e. operational data we do not have yet |
| Cross-frame consensus | A single noisy frame stops deciding anything | Requires multiple frames per student, which the scan planner must guarantee |
| Lower auto-accept threshold *plus* mandatory confirmation | Trades automation for accuracy — the system asks more but wrongly marks fewer present | More operator load. Quantified in docs/benchmarks.md |

**The honest residual:** if SFace genuinely cannot separate two particular
students at any threshold, no amount of decision-layer engineering recovers it.
That pair goes to the human queue forever until better embeddings are available.
The correct response is to measure the per-pair confusion matrix and surface the
worst offenders, not to tune until the average looks good.

### Option 3 — Train our own

Only viable with **first-party consented data** from enrolled students, which
we collect anyway. Realistically months, and it competes with option 1 on
budget. Its genuine advantage: training-data provenance is airtight by
construction, which retires the SFace caveat permanently.

### Option 4 — AWS Rekognition (managed)

Prices below were **fetched from <https://aws.amazon.com/rekognition/pricing/> on
2026-09-29** (MEASURED). Note the unit: Rekognition Image is billed **per image
processed**, tiered by monthly volume — *not* per detected face.

| API group | APIs | First 1M images/month | Next 3M |
|---|---|---|---|
| **Group 1** | `IndexFaces`, `SearchFacesByImage`, `SearchUsersByImage`, `CompareFaces`, `AssociateFaces`, `DisassociateFaces`, `SearchFaces`, `SearchUsers` | **$0.0010 / image** | **$0.0008 / image** |
| **Group 2** | `DetectFaces`, `DetectLabels`, `DetectModerationLabels`, `RecognizeCelebrities`, … | **$0.0010 / image** | **$0.0008 / image** |
| Image Properties | property extraction | $0.00075 / image | $0.0006 / image |
| Face metadata storage | face vectors + user vectors | **$0.00001 / vector / month** | — |

Free tier (first 12 months): 1,000 images/month in Group 1 **and** Group 2, plus
1,000 face vectors and 1,000 user vectors/month.

**Cost per room per year.** Volume assumptions are ESTIMATE (stated below the
arithmetic, not measured):

```
ASSUMPTIONS (ESTIMATE)
  students per room              = 300
  frames per scan (8 angles)     = 8
  scans per school day           = 3
  teaching days per year         = 250

per scan:
  DetectFaces        8 images x $0.0010 = $0.008   (Group 2)
  SearchFacesByImage 8 images x $0.0010 = $0.008   (Group 1, after enrollment)
                    ----------------------------------
  per scan                                 = $0.016

per year:
  scans/room/year = 3 x 250                 = 750
  API cost        = 750 x $0.016            = $12.00
  face storage    = 300 students x 15 vectors x $0.00001/mo x 12
                                                 = $0.54
                    ----------------------------------
  TOTAL, one room per year                   = ~$12.54   (ESTIMATE)
```

**Correction worth flagging.** An earlier draft of this document claimed
`$0.0025 per face matched`, giving ~$4,500 per room per year and arguing
self-hosting was necessary on cost grounds. **That figure was wrong** — it was
recalled, not fetched. The correct figure is **~$12.54 per room per year**, and
it is roughly *the same order as the electricity for the edge computer*. Cost
is therefore **not** a reason to prefer self-hosting.

The real objections to Rekognition remain, and they are serious:

- **Privacy and residency.** Face images leave the customer's tenancy and enter
  AWS's. For an Indian college customer that raises data-residency and
  cross-border-transfer questions under the DPDP Act 2023, and it changes the
  customer's data-processing agreement. **NEEDS LAWYER.**
- **Vendor lock-in.** The gallery becomes a Rekognition Face Collection. Moving
  to another engine later means re-enrolling everyone.
- **Student-record liability in a third-party account.** A mistake or a breach
  at the vendor is the vendor's to answer, not ours — but the regulator asks
  the controller (the college), which is our customer. Commercial risk.
- **Liveness.** `DetectFaceLiveness` is a **separate, additional** charge and is
  not included in the figures above.

**Revised recommendation:** self-host the permissive baseline as the default
(privacy sovereignty is worth more than $12/room/year), but keep Rekognition as
a genuinely cheap, credible fallback — which it is. If a customer has an
acceptable AWS posture and wants accuracy without a licence purchase, this is a
low-cost pilot route.

## 4. How the code enforces this

The guard is not documentation — it is a start-up assertion, and it is tested
adversarially (`tests/test_model_registry.py`, 20 tests).

```
app/registry/models.py     ModelDescriptor + LicenseMetadata + ModelRegistry
                           assert_production_licensing() — the guard
app/registry/loader.py     the ONLY place a backend is constructed
app/main.py                calls load_registry() during lifespan startup
```

Every descriptor carries: `license_name`, `commercial_use`, `training_data`,
`source_url`, `sha256`, `notes`, `legal_review_required`.

**Production behaviour (MEASURED by test):**

```
ENVIRONMENT=production DETECTOR_BACKEND=insightface_buffalo_l
  -> NonCommercialModelError, process exits non-zero, before any weight is loaded

ENVIRONMENT=production DETECTOR_BACKEND=opencv_yunet EMBEDDER_BACKEND=opencv_sface
  -> starts
```

The guard fires **before** backend construction, so a production deployment
cannot even *download* non-commercial weights.

## 5. One deliberate engineering trade, recorded

`legal_review_required` (SFace's undocumented training corpus) is **advisory,
not a blocker.**

Rationale: it is the only commercially usable embedder available today.
Blocking on it makes the product unshippable, which means no revenue, no pilots
and no evidence that the rest of the system works. The risk is instead surfaced
loudly — logged at WARNING, returned by `GET /health/models`, listed in
`docs/HUMAN_ACTIONS.md` item 2 — so it cannot be forgotten.

This is a trade between two kinds of harm and it is **not a legal conclusion**.
It is pinned by
`test_outstanding_legal_review_does_not_block_startup` so that nobody changes
it accidentally. **NEEDS LAWYER before commercial launch.**

## 6. Swap path

To change models you change configuration, not code:

```bash
# baseline (current default)
DETECTOR_BACKEND=opencv_yunet
EMBEDDER_BACKEND=opencv_sface

# once a commercial InsightFace licence is purchased, record it and enable:
cat > /etc/attendance/models.json <<'JSON'
{
  "models": {
    "licensed_placeholder": {
      "version": "buffalo_l-commercial-2026",
      "license": {
        "license_name": "commercial-licensed",
        "commercial_use": true,
        "training_data": "first-party-consented",
        "source_url": "contract://<your-contract-reference>",
        "sha256": "<sha256 of the licensed weights>",
        "legal_review_required": false
      }
    }
  }
}
JSON
MODEL_REGISTRY_CONFIG=/etc/attendance/models.json
DETECTOR_BACKEND=licensed_placeholder
EMBEDDER_BACKEND=licensed_placeholder
```

Then implement `build_detector` / `build_embedder` in
`app/registry/backends/licensed_stub.py` (or a new module) and register the key.

**Switching the embedder invalidates every stored embedding.** `face_gallery`
rows are 128-d SFace vectors today; ArcFace vectors are 512-d and live in a
different space. The system detects a dimension mismatch and refuses rather than
silently producing garbage, but you must then re-enroll:

```bash
alembic upgrade head
POST /students/reembed            # added in W6; re-derives from stored crops
# or, if crops were purged, re-run enrollment from ENROLL_PHOTOS/
```

**This is the single largest operational cost of a model swap and must be in any
pilot plan.** It is also why the embedder version is recorded per gallery entry
in W6 — so a future swap can re-embed only what is actually stale.
