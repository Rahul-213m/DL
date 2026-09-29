# ADR 0008 — Three credentials, strictly separated

- **Status:** Accepted
- **Date:** 2026-09-29

## Context

The legacy system had exactly one credential: a shared API key in `.env`,
compared with `!=`, identical for every operator. Two consequences:

1. **No accountability.** `resolved_by` was a form field any operator typed.
   The audit trail recorded whoever was believed to be present, which makes it
   worthless as evidence.
2. **No least privilege.** A read-only viewer and a college admin held the same
   authority, and so did the edge device (once it existed).

## Decision

Three credential types, with disjoint authority.

| Credential | Holder | Lifetime | Authority |
|---|---|---|---|
| **User JWT** | a person | 8 h | admin / teacher / read-only, by capability |
| **Device token** | an edge node | 1 year | `frames:upload` and nothing else |
| **API key** | server-to-server bootstrap | until rotated | provisioning only |

### Rules enforced in code, not documented

1. **The actor always comes from a verified credential.** Audit rows are built
   by `TenantContext.audit()`, which reads `Actor.actor_id`. A request body
   cannot influence it, because the request body is never consulted.
2. **Constant-time comparison for every secret.** `hmac.compare_digest` for
   opaque secrets, bcrypt for passwords. The legacy `!=` leaks its prefix
   through timing.
3. **A device is refused every human capability**, regardless of its role. Its
   default role is READONLY, so without an explicit branch a compromised edge
   node could read the student roster. *This was a real gap found by a test
   during W4.*
4. **Capability table, not scattered role checks.** `CAPABILITIES` maps each
   capability to a minimum role. A new endpoint answers one question — "what
   is the minimum role here?" — instead of being audited branch by branch. An
   unknown capability **raises**, so a typo in a decorator stops the request
   rather than granting access.
5. **JWT algorithm is pinned** and `exp`/`sub`/`tid`/`role` are required claims,
   so an `alg=none` forgery or a tenant-less token is rejected. Tested.

## Why not OIDC

It is the right long-term answer and the design does not preclude it: the
`Actor` abstraction is the only thing handlers consume, so swapping JWT for an
OIDC introspection changes one module. It is not first because no college
customer has an identity provider we can test against, and shipping an
unverifiable auth integration is worse than shipping a verifiable one.

**Revisit when the first customer contract requires SSO.**

## Consequences

- Passwords use bcrypt at cost 12. That is ~250 ms per hash, which is correct
  for a login and wrong for a hot path. Device tokens therefore use SHA-256
  instead: they are 256-bit random values, not user-chosen, so there is
  nothing to brute-force and bcrypt's slowness would only slow every upload.
- The legacy `require_api_key` shim remains for the pre-tenant endpoints and is
  marked for removal in W7. It is not extended.
