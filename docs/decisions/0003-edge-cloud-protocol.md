# ADR 0003 — Edge-to-cloud: presigned multipart upload, not a streaming API

- **Status:** Accepted
- **Context:** Edge nodes sit on unreliable campus Wi-Fi behind NAT. They must
  upload multi-megabyte classroom frames, survive restarts, work for hours with
  the network down, and never double-count an attendance event.
- **Decision:** The edge uploads **directly to S3 with a presigned multipart
  URL**, then POSTs a small JSON manifest to the cloud API. The cloud API never
  proxies image bytes.
- **Rationale:**
  - CloudFront/S3 multipart uploads are resumable byte-range by construction, so
    a dropped connection resumes from the last committed part rather than
    restarting.
  - It avoids double egress: bytes go phone -> edge -> S3 once, not
    phone -> edge -> cloud API -> S3.
  - The manifest is tiny, so the API can be synchronous and strongly validated.
  - Presigned URLs expire, so a compromised edge node cannot write forever.
- **Idempotency:** The manifest carries a client-generated `frame_id` (UUIDv7)
  and a SHA-256 of the image. The cloud inserts with `ON CONFLICT DO NOTHING` on
  `frame_id`, so a retried upload is a no-op. A retried *decision* is
  idempotent by construction (see ADR 0006).
- **Ordering:** SQS FIFO per-tenant ordering, deduplication by `frame_id`,
  with the manifest's own `captured_at` used for attendance timing — never the
  server receipt time.
- **Auth:** each edge device has its own long-lived credential
  (`device_tokens`), scoped to upload only. A stolen device credential cannot
  read any other tenant's data. See ADR 0008.
- **Rejected:**
  - gRPC streaming through the API: no resumability, double egress, and the API
    becomes a bandwidth bottleneck.
  - MQTT for image transfer: same problems, plus a broker to operate.
  - Direct S3 SDK from edge without presigning: requires shipping cloud
    credentials to the classroom.
- **Fallback:** if the cloud is unreachable, the edge writes manifests to a
  SQLite outbox on the classroom device and drains it on reconnect.
