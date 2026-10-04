"""Operator command to requeue captures after correcting a permanent failure."""

from __future__ import annotations

import argparse
from pathlib import Path

from edge_uploader.outbox import EdgeOutbox


def main() -> None:
    """Requeue failed captures without deleting their local image data."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", default="/var/lib/attendance")
    parser.add_argument("--tenant-id", required=True)
    parser.add_argument("--device-id", required=True)
    args = parser.parse_args()

    outbox = EdgeOutbox(
        root=Path(args.data_root),
        tenant_id=args.tenant_id,
        device_id=args.device_id,
    )
    count = outbox.requeue_failed()
    print(f"Requeued {count} failed capture(s); no image files were deleted.")


if __name__ == "__main__":
    main()