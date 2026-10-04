# Edge-to-Cloud Deployment and Operations

This guide connects the ROS 2 classroom device to the FastAPI attendance service over the public internet. The supported production path is AWS-backed: PostgreSQL, private S3 with customer-managed KMS encryption, and SQS configuration. The ROS device initiates HTTPS requests outbound; ROS/DDS is never exposed to the internet.

## 1. Data path and identifiers

```mermaid
flowchart LR
    C[Camera bridge] -->|durable JPEG + journal| O[(Local edge outbox)]
    O --> U[Edge uploader]
    U -->|HTTPS 443, multipart frame| I[Cloud ingress / TLS]
    I --> A[FastAPI /v1/sessions/{id}/frames]
    A --> D[(Tenant-scoped PostgreSQL)]
    A --> S[(Private S3, SSE-KMS)]
    A --> Q[SQS, when async queue adapter is implemented]
    A --> P[Perception and identity]
```

The edge and cloud have separate runtimes by design: ROS 2 Jazzy/Python 3.12 at the classroom; Python 3.13/FastAPI in the cloud. The camera writes captures to a local durable outbox. The uploader retries from that outbox and sends JPEG multipart requests to `POST /v1/sessions/{cloud_session_id}/frames` using `X-Device-Id` and `X-Device-Secret`.

There are three different identifiers; do not interchange them:

- `tenant_id` scopes the cloud tenant and comes from the verified device credential. The edge's local `tenant_id` parameter is not an authorization claim.
- `cloud_session_id` is the numeric session returned by the cloud's `POST /v1/sessions` endpoint. It must be open before uploads.
- The ROS scan `session_id` is a local scan correlation string. It is retained in the outbox but is not the cloud session ID.

Frame idempotency uses the durable capture ID as `frame_id`. Repeating an upload after a timeout is expected; the cloud returns the existing result for a duplicate frame ID. TLS protects the image and device credential in transit. There is no inbound ROS control channel in this design.

## 2. Network and cloud prerequisites

Provision the cloud API behind a DNS name and an HTTPS ingress/load balancer with a publicly trusted certificate. Configure ingress to forward to the API on its private network. Permit inbound internet traffic only on TCP 443 at the ingress. Permit edge-initiated DNS and TCP 443 to the API hostname; do not configure port forwarding, public SSH, public PostgreSQL, public S3 objects, or public ROS/DDS ports for the classroom device.

Set ingress request-body allowance to at least `MAX_UPLOAD_BYTES` plus multipart overhead (default image limit is 25 MiB). Set the ingress/API request timeout from measured inference latency; a timeout after server acceptance is safe to retry because frame IDs are idempotent. Restrict API administrative endpoints to operator identities and, where possible, an administrative access network.

The production API configuration must include:

- `ENVIRONMENT=production`, PostgreSQL `DATABASE_URL`, and independent high-entropy `API_KEY` and `JWT_SECRET` values.
- `STORAGE_BACKEND=s3`, a private `S3_BUCKET`, correct `S3_REGION`, and `S3_KMS_KEY_ID`. Use a workload IAM role; do not put AWS access keys in the edge config or image.
- `JOB_QUEUE_BACKEND=sqs` and `SQS_QUEUE_URL` per the current configuration guards.
- Commercial-use model approval, consent/retention operations, encrypted backups, alerting, and a tested recovery plan.

The Compose file is a single-host starting point, not a highly available production architecture. It binds the API to loopback so an HTTPS ingress can sit in front, persists PostgreSQL in a named local volume, and runs Alembic before the API. Use managed PostgreSQL, durable backups, a managed container runtime, IAM workload identity, and a separately managed HTTPS ingress for a real service. The deployment owner must attach least-privilege permissions for S3/KMS and SQS.

Before rollout, verify runtime support rather than relying only on configuration names: the current codebase has an in-memory job-queue implementation and production settings require `sqs`, but no SQS consumer/producer adapter is wired into the application. Likewise, the edge uploads multipart directly to FastAPI; the presigned-object-upload design is not implemented. Do not claim durable asynchronous cloud processing or horizontal inference scaling until those paths are implemented and load-tested. See [Production gates](#8-production-gates).

## 3. Provision tenant, room, class, and device

Run these operator actions against the HTTPS API or the authenticated operator console. The first account can be created using the existing signup flow; later accounts must be invited/created by a tenant administrator.

1. Create the tenant's first admin with `POST /v1/auth/signup` and sign in with `POST /v1/auth/signin`. Store the returned bearer token only in the operator's secret store. Never place a human JWT on the edge.
2. As a tenant admin, create the physical room with `POST /v1/admin/rooms`, recording measured width, depth, camera height, and seat count. Create the class with `POST /v1/people/classes`, passing the returned `room_id`.
3. Import the roster, record granted consent, add consenting students to the class, and complete gallery enrollment. Frames received without an eligible consented class roster cannot produce valid identity attendance.
4. Create one upload-only edge device with `POST /v1/admin/devices`, for example `{"name":"Room 204 attendance edge","scopes":["frames:upload"]}`. Store `device_id` and the one-time `device_secret` immediately in an approved secret manager. The API stores only a hash of the secret. The device starts pending.
5. Activate the device with `POST /v1/admin/devices/{device_id}/active`. Confirm it appears active in `GET /v1/admin/devices`.
6. At the beginning of a class period, create an open session with `POST /v1/sessions` and body `{"class_id":"<class_id>"}`. Record its numeric `session_id`; it is the edge's `cloud_session_id`. Close the session after the capture/retry window using `POST /v1/sessions/{session_id}/close`.

Do not keep one session ID in service indefinitely. Closed sessions reject frames. For a new period, open a new cloud session and update the edge parameter before scanning. Until the deployment implements an authenticated session-control/scheduling protocol, session creation and rotation are operator actions.

## 4. Install edge credentials and configure ROS

On the classroom Linux device, install ROS 2 Jazzy and build this repository's `ros_ws` with its supported build script. Create the secret file as the ROS service account; it must be a regular file with mode `0600` or the uploader refuses to use it:

```bash
sudo install -d -o attendance -g attendance -m 0700 /etc/attendance
read -rsp "Device secret: " DEVICE_SECRET; printf '\n'
printf '%s' "$DEVICE_SECRET" | sudo install -o attendance -g attendance -m 0600 /dev/stdin /etc/attendance/device-secret
unset DEVICE_SECRET
```

Edit only the `[INSTALL]` entries in `ros_ws/src/attendance_bringup/config/edge.yaml` (or the installed copy under the ROS package share):

- `camera_bridge.driver`, `ip_webcam_host`, and camera port for the commissioned camera.
- `servo_controller.driver`, serial port, measured motion limits, and feedback setting for the installed actuator.
- `edge_uploader.base_url` to the HTTPS origin only, for example `https://attendance.example.edu` (no `/v1` suffix).
- `edge_uploader.device_id` to the activated device ID, `cloud_session_id` to the currently open numeric cloud session, and `device_secret_file` to the secret file above.
- Set both camera and uploader `outbox_data_root`/`data_root` to the same persistent local filesystem path. Set matching local tenant/device parameters for clear local diagnostics; the API derives tenant authorization from the device secret, not these values.
- Measure room dimensions, camera geometry, servo range, and optical zoom. Do not copy the sample room geometry or assume digital zoom provides detail.

Homing is not automatic at startup. Before any movement, clear the mechanism's full travel envelope and deliberately home it with the servo action. Without position feedback, homing does not verify the true angle and stall detection is unavailable; an external, hard-wired power cut remains necessary for physical safety.

Protect the edge OS account and disk: queued photographs are biometric data at rest. Use encrypted full-disk storage, disable unattended debug access, apply OS security updates, restrict `/var/lib/attendance` to the service account, and define local outbox deletion and device-retirement procedures.

## 5. Verify before a real scan

From the edge, confirm DNS, certificate validation, and outbound access:

```bash
curl --fail --show-error --silent https://attendance.example.edu/health
```

Do not use `curl -k` or disable certificate verification. Check that the API reports ready before commissioning and that the configured session is still open. Then build and run simulation before connecting hardware:

```bash
cd ros_ws
./build.sh
source install/setup.bash
ros2 launch attendance_bringup edge.launch.py mode:=simulated
```

The shipped simulated profile intentionally has no real device secret and `cloud_session_id: 0`; it writes test captures locally and must not upload them to a tenant. For a controlled cloud integration test, provision a dedicated test tenant/device/session and configure a test-only profile with those credentials. Confirm all of the following before switching to hardware:

- `GET /health` succeeds from the edge and the TLS certificate is trusted.
- The uploader logs accepted frame IDs and queue depth returns to zero.
- Cloud session detail/reporting shows ingested frames and expected test attendance; a duplicate retry does not create duplicate frame/event rows.
- Invalid/rotated device secrets are rejected; a device cannot read rosters or another tenant's data.
- Stopping internet access leaves captures pending locally; restoring access drains them without operator re-enqueue.
- A closed or wrong-tenant session is rejected and is visible in uploader error/queue state.
- The camera, servo, stop behavior, image sharpness, room coverage, and physical safety are separately checked with the hardware in a supervised, unoccupied test area.

The current uploader treats non-5xx HTTP errors as permanent after one attempt. Correct session/device/configuration errors, then explicitly requeue failed captures without deleting images:

```bash
source /opt/ros/jazzy/setup.bash
source ros_ws/install/setup.bash
sudo -u attendance ros2 run edge_uploader edge_requeue_failed --data-root /var/lib/attendance --tenant-id '<local-diagnostic-tenant-id>' --device-id '<device-id>'
```

Ensure the configured request timeout covers measured API processing. Queue depth and disk free space should be monitored together.

## 6. Failure and recovery procedures

**Internet outage:** Keep scanning only while the local disk has capacity and the consent/privacy policy allows local retention. The outbox retries when connectivity returns. Never expose a ROS topic, DDS discovery, camera port, or database port to make uploads work.

**Queue not draining:** Check edge DNS/TLS and `/health`, then check the API `/ready`, the open session, device active state, and device ID/secret pairing. HTTP 401/403 usually means credentials/device state; 404/409 commonly means an invalid/closed session; 413 means the API/ingress image limit is too small. Inspect edge uploader logs and outbox stats before requeueing.

**Lost or suspected leaked device secret:** Revoke the device immediately with `POST /v1/admin/devices/{device_id}/revoked`, rotate via `POST /v1/admin/devices/{device_id}/rotate`, replace the root-protected file, and verify the device remains tenant-scoped. A rotation invalidates the old secret.

**Edge replacement:** Preserve or securely dispose of the encrypted outbox according to retention policy. Provision a new device identity; do not clone a secret to a different room. Update the device ID and secret file together.

**Cloud rollback/recovery:** Back up PostgreSQL and the S3 data with encryption and tested restore procedures. Run migrations as a controlled release step and take a database backup before schema changes. Do not run multiple independent migration jobs concurrently.

## 7. Security and privacy operating requirements

Faces and embeddings are sensitive biometric data. Obtain the legally required notice/consent and institutional approvals before enrollment or capture; grant consent in the tenant system and honor withdrawal/erasure requests. Use least-privilege user roles, upload-only device scope, TLS, KMS-backed S3 encryption, encrypted database/backups, audit-log review, retention jobs, and incident-response contacts. Restrict the operator API and logs; never log frame bytes, device secrets, bearer tokens, or full presigned URLs. Treat model licensing, demographic performance evaluation, false-match acceptance criteria, and human review staffing as release gates, not post-launch cleanup.

The product does not currently provide liveness/anti-spoof protection. Do not describe it as spoof-resistant or rely on face matching as the only attendance control. Keep a human correction path and an alternative accessible attendance method.

## 8. Production gates

This repository is not yet a fully production-ready internet service. The following are verified gaps requiring completion and acceptance before a production launch:

- Implement and test the configured SQS job-queue backend and worker lifecycle; production configuration currently checks for `sqs`, but the application code only contains the in-memory queue and no wired SQS producer/consumer was found.
- Decide whether inference is synchronous or queued. The current frame endpoint invokes ingestion in the request path despite returning HTTP 202; benchmark worst-case 4K latency and set timeouts/capacity accordingly. Implement durable asynchronous processing before multi-replica scaling.
- Implement the planned presigned object upload path if image sizes/uplink cost require it. Current edge transport sends multipart images through the API.
- Validate cloud schema migrations, managed database HA/PITR, S3/KMS IAM policies, queue permissions, backups, restore drills, WAF/rate limits, secrets rotation, alerting, and incident response in the target account.
- Complete real camera/servo commissioning, hardware emergency-stop and fault-injection tests, full-room face coverage, offline-duration/disk-capacity tests, performance/accuracy evaluation, licensing review, and privacy/legal review.
- Provide an operator session lifecycle or scheduler before unattended daily operation; today the cloud session ID must be created and configured for each class period.

Local validation is not a substitute for these deployment and policy approvals. Track acceptance evidence and owners in `docs/HUMAN_ACTIONS.md` and the institution's release record.