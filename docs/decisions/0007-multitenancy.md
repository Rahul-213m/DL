# ADR 0007 — Multi-tenancy: shared database, `tenant_id` discriminator

- **Status:** Accepted (operator decision: "multi-tenant with strict per-tenant
  data isolation")
- **Date:** 2026-09-29

## Context

The product is sold to many colleges. Two of them having students with the same
roll number is not an edge case; it is the normal case. The pre-W4 schema has no
notion of ownership, so college A's attendance and college B's attendance are the
same rows. That is unshippable, and once there are two customers it is a
reportable breach.

The requirement is **strict** isolation, which rules out "isolation by
convention" — a policy that works if every developer remembers.

## Decision

**Shared database, shared schema, `tenant_id` on every tenant-owned table,
enforced in three layers:**

1. **Schema.** Every tenant-owned table has a non-null `tenant_id` with an
   index leading with it.
2. **Database.** Composite foreign keys — `(tenant_id, class_id)` →
   `classes(tenant_id, class_id)` — mean a child row **cannot** reference a
   parent in another tenant. This is a storage guarantee, so a bug in one
   service cannot leak data across a college boundary.
3. **Application.** `app/services/tenancy.py` is the only sanctioned data
   access path. Every function takes the tenant id explicitly, so *forgetting*
   the filter is a signature change rather than a silent leak.

Two structural tests enforce the invariant at test time: every tenant-owned
table must have a `tenant_id`, and must have an index leading with it.

## Alternatives considered

| Option | Why rejected |
|---|---|
| **Database per tenant** | Strongest isolation. Rejected for launch: 200 colleges means 200 databases, 200 migrations, 200 backup jobs, and a cross-college aggregate query becomes a distributed join. The infrastructure cost is a real product cost for a company selling to colleges that will each have 20–50 rooms, not 200 campuses. Reconsider at >1,000 tenants or when a customer contractually requires physical separation — the ADR would be reopened, not ignored. |
| **Schema per tenant** | No extra database, but 200 schemas makes every migration 200 statements, and a bug in the migration is 200 bugs. Worse than database-per-tenant without the isolation benefit. |
| **Application-level filtering only** | Rejected. This is the option the legacy code was closest to and the reason it is unsafe: one forgotten `where` clause is a breach, and nothing catches it. The composite FKs exist specifically so that "only the application" is not the answer. |

## Consequences

- **Email is unique per tenant, not globally.** The same person may be an admin
  at one college and a read-only viewer at another.
- **Roll numbers are unique per tenant.** `R1` exists once per college.
- **The vector index is per tenant.** `app/services/vector_index.py` is
  instantiated per tenant context, not shared. A shared index across tenants
  would let a similarity search return another college's student.
- **Migrations are the one global operation.** A schema change touches every
  tenant. This is the main cost of the shared-schema choice, accepted because
  it makes the alternative (200 migrations) far worse.
- **Analytics across tenants** must go through a separate, explicitly audited
  path. There is deliberately no such path yet, because "which colleges are
  adopting this?" is a question answered by sales, not by a query that could
  leak one college's roster into another's view.

## Cross-tenant testing

`tests/test_tenancy.py` is written adversarially: two tenants with
*deliberately identical* roll numbers, because a missing filter then returns
the wrong row silently instead of raising. Every single-tenant getter is
parametrised against a foreign primary key.

## Compliance note

Under the DPDP Act 2023, isolation between data fiduciary customers is a
contractual and potentially statutory requirement, not a feature. **NEEDS
LAWYER** to confirm that logical isolation in a shared database satisfies the
customer-facing commitments. See `docs/compliance.md`.
