# Consented Evaluation Data Protocol

This protocol is for measuring face-embedding similarity and selecting a
candidate similarity threshold. It is not a substitute for institutional
privacy review, consent records, or a deployment risk assessment. Do not collect
or process student images until the institution has approved the purpose,
retention period, access controls, and withdrawal procedure.

## Collection Rules

- Obtain and record explicit, purpose-specific consent before enrollment or
  evaluation capture. Exclude pending or withdrawn consent from collection,
  gallery construction, and evaluation.
- Use a controlled evaluation set separate from training, tuning, and operator
  practice. Record the consent reference outside the evaluation CSV; never put
  names, roll numbers, emails, or other direct identifiers in the report.
- Assign pseudonymous `subject_id`, `probe_id`, and `session_id` values. Keep
  the re-identification key separately, encrypted, and accessible only to the
  designated data steward.
- Split by capture session before generating pairs. A `session_id` may appear
  in `calibration` or `test`, never both. Prefer a later date/term for the test
  split so lighting, pose, and appearance drift are represented.
- Include genuine same-identity pairs and impostor different-identity pairs.
  Sample impostors across identities and sessions; do not count the same image
  pair repeatedly. Record the number of distinct subjects, probes, sessions,
  and pairs when interpreting uncertainty.
- Keep the detector, embedder, preprocessing, alignment, and model weights
  fixed for a run. Record the exact model version/hash. A model or preprocessing
  change requires a new evaluation.
- Store raw images and embeddings only in approved encrypted storage with
  access logging and a documented deletion date. The CSV below contains scores
  and pseudonymous identifiers, but it is still sensitive biometric-derived
  data and must receive the same access and retention protections.

## Score File

Create a UTF-8 CSV with one row per genuine or impostor comparison and these
columns:

| Column | Meaning |
|---|---|
| `sample_id` | Unique ID for this comparison row. |
| `split` | Exactly `calibration` or `test`. |
| `label` | Exactly `genuine` or `impostor`. |
| `score` | Cosine similarity, normalized to the range 0 through 1. |
| `session_id` | Pseudonymous capture session for the probe image. |
| `model_version` | Immutable model/preprocessing identifier, preferably including a weight hash. |

Example (synthetic values only):

```csv
sample_id,split,label,score,session_id,model_version
p01-g,calibration,genuine,0.83,session-2026-01,opencv-sface-sha256:abc123
p01-i,calibration,impostor,0.31,session-2026-01,opencv-sface-sha256:abc123
p02-g,test,genuine,0.79,session-2026-02,opencv-sface-sha256:abc123
p02-i,test,impostor,0.42,session-2026-02,opencv-sface-sha256:abc123
```

Generate scores from the same frozen pipeline and record the mapping from each
comparison to its pseudonymous probe and subject in a separately controlled
manifest. Keep pair sampling consistent with the intended operating use; a
pair-level false-accept rate is not the same quantity as the probability that
an entire classroom scan marks an absent student present.

## Evaluation

Run the evaluator with the score file and a predeclared FAR target:

```bash
python scripts/evaluate.py scores.csv --far-target 0.001 --json evaluation.json
```

The evaluator chooses a candidate threshold using only the `calibration` split,
then reports TAR, FAR, FRR, ROC AUC, and sample counts on both splits at that
fixed threshold. Its output is a development measurement, not a guarantee. A
small sample may show zero false accepts without supporting a low-FAR claim;
report warnings and denominators, not just the rounded rate. Never tune on the
test split and then report that same split as independent evidence.

## Retention and Withdrawal

Document the data owner, purpose, consent evidence location, access list,
retention date, and deletion verification method before collection. On consent
withdrawal, stop future processing immediately and remove the subject's images,
embeddings, and derived score rows where required by the approved policy. Keep
only the minimum non-biometric audit record required by the institution and
law. Verify deletion from primary storage, replicas, backups, exports, and
developer workstations; record what cannot be removed and its expiry date.