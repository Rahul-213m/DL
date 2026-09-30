#!/usr/bin/env python3
"""Print the pixels-per-face table for a camera and a set of distances.

    ros2 run scan_planner show_face_sizes
    ros2 run scan_planner show_face_sizes --fov 70 --width 4608 --max-zoom 4

This exists because the number that decides whether the hardware is adequate
(``docs/hardware/pixels_per_face.md``) is a derived one, and a derived number
that nobody can reproduce is a number nobody trusts. It prints the same
arithmetic the planner uses.
"""

from __future__ import annotations

import argparse

from scan_planner.planner import DETECT_FACE_PX, IDENTIFY_FACE_PX, RoomGeometry, expected_face_px


def main(args: list[str] | None = None) -> None:
    """Print the table."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fov", type=float, default=70.0, help="horizontal FOV in degrees")
    parser.add_argument("--width", type=int, default=4608, help="still width in pixels")
    parser.add_argument("--max-zoom", type=float, default=4.0, help="largest optical zoom")
    parser.add_argument("--distances", type=float, nargs="*", default=[2, 3, 5, 6, 8, 10, 12, 15, 20])
    parser.add_argument(
        "--room",
        type=float,
        nargs=2,
        metavar=("DEPTH_M", "WIDTH_M"),
        help="also report what one specific room needs",
    )
    options = parser.parse_args(args)

    zooms = [1.0, 2.0, 4.0]
    header = "distance | " + " | ".join(f"{z:g}x" for z in zooms)
    print(f"FOV {options.fov:g} deg, {options.width} px wide, max optical zoom {options.max_zoom:g}x")
    print(f"floors: detect {DETECT_FACE_PX:g} px, identify {IDENTIFY_FACE_PX:g} px")
    print(header)
    print("-" * len(header))
    for distance in options.distances:
        cells = []
        for zoom in zooms:
            if zoom > options.max_zoom:
                cells.append(f"{'n/a':>5}")
                continue
            size = expected_face_px(distance, fov_deg=options.fov, frame_width_px=options.width, zoom=zoom)
            mark = "*" if size >= IDENTIFY_FACE_PX else ("+" if size >= DETECT_FACE_PX else " ")
            cells.append(f"{size:5.0f}{mark}")
        print(f"{distance:8.0f}m | " + " | ".join(cells))
    print("\n* identifies   + detects only")

    if options.room:
        show_room(options.room[0], options.room[1], options.fov, options.width)


def show_room(depth_m: float, width_m: float, fov: float, width_px: int) -> None:
    """Show what a specific room needs."""
    room = RoomGeometry(depth_m=depth_m, width_m=width_m, horizontal_fov_deg=fov)
    far = room.far_corner_distance()
    size = expected_face_px(far, fov_deg=fov, frame_width_px=width_px)
    needed = IDENTIFY_FACE_PX / size
    print(f"\nRoom {depth_m:g}m x {width_m:g}m, worst-case subject {far:.1f}m away -> {size:.0f} px")
    if needed <= 1.0:
        print("  identifies at 1x. No optical zoom needed.")
    elif needed <= room.max_zoom:
        print(f"  needs {needed:.1f}x OPTICAL zoom to identify. Digital zoom will not help.")
    else:
        print(
            f"  needs {needed:.1f}x optical but only {room.max_zoom:g}x exists. "
            f"THIS CAMERA CANNOT SCAN THIS ROOM."
        )


if __name__ == "__main__":
    main()
