# Pixels per face: does this camera work in this room?

**Status: DERIVED FROM A DOCUMENTED MODEL, NOT MEASURED ON HARDWARE.**
The model is the pinhole relation. The inputs (sensor size, focal length,
field of view) are plausible phone values, not a measured device. The
conclusion is directional and robust; the exact thresholds are not.

## The question

Recognition quality depends on how many pixels wide a face is in the frame.
The cloud's quality gate (`app/core/domain/imageops.py`) rejects a face below
80 px because below that the embedding is dominated by quantisation.

So: **at the back of a real classroom, does a phone camera clear 80 px?**

## The model

For a pinhole camera, an object of physical width `W` at distance `d` subtends
`W / d` radians, and the focal length in pixels `f` converts that to pixels:

```
face_px = f * W / d
f = (frame_width_px / 2) / tan(hfov / 2)
```

A typical adult face is `W ≈ 150 mm`. A phone main camera is typically
`hfov ≈ 70°` on a 4608 px wide still.

## The numbers

| Distance | face_px at 1x | at 2x | at 4x |
|---------:|-------------:|------:|------:|
| 2 m | 247 | 494 | 987 |
| 5 m |  99 | 197 | 395 |
| 8 m |  62 | 124 | 247 |
| 12 m |  41 |  82 | 165 |
| 20 m |  25 |  49 |  99 |

Reproduce with:

```bash
ros2 run scan_planner show_face_sizes
```

## What this means

1. **A phone at the front of a room is excellent.** 247 px at 2 m is far more
   than the 80 px floor, and quality will not be resolution-limited.

2. **At 8 m, a phone at 1x is below the floor (62 px).** This is the
   important line in the table. The middle of a lecture hall is already
   marginal.

3. **Optical zoom fixes it; digital zoom does not.** At 8 m, 2x optical gives
   124 px, comfortably clear. Digital zoom interpolates existing pixels: it
   makes a 62 px face 124 px wide without adding one pixel of information, and
   the embedding is *worse*, not better, because the interpolation smooths
   exactly the high-frequency detail a face embedding keys on.

4. **The system detects at 30 px and identifies at 80 px.** These are different
   floors and conflating them is a design error: a 62 px face is findable but
   not identifiable, and that is exactly the case that should trigger a
   targeted tele retake. `scan_planner` models this with
   `DETECT_FACE_PX` and `IDENTIFY_FACE_PX`.

## The hardware decision this forces

- **The camera needs a motorised optical telephoto.** Without one, a room
  deeper than about 6 m cannot be identified, and no software change will
  help. `scan_planner` says so explicitly when given a fixed-lens camera.
- **The camera must not be the phone's ultra-wide.** A 120° FOV at 4608 px
  gives `f = 1383`, and a 12 m face is 17 px: undetectable.
- **A fixed-focus lens is preferable**, or AF must be locked after focusing.
  An AF search at the start of a sweep blurs the first several frames.

## To replace this model with a measurement

1. Mount the camera at the intended height at the front of the real room.
2. Seat one person at the BACK row, at a recorded distance.
3. Capture a still. Measure the inter-ocular distance in pixels; face width is
   about 2.3x that.
4. Compare against the table. If the real number is much lower than the model,
   the field of view is narrower than assumed and the zoom requirement rises.

Record the result in `docs/benchmarks.md` and update
`cam_bridge`'s `SimulatedCamera` so the simulation stops lying.
