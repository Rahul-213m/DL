# ADR 0004 — Hexagonal core: domain logic imports nothing

- **Status:** Accepted
- **Context:** The legacy `routes.py` was 597 lines mixing HTTP parsing, business
  rules, SQLAlchemy queries and FAISS calls. Business rules could only be tested
  through a TestClient with a live database.
- **Decision:** `app/core/domain/` imports **only** numpy and the standard
  library. It depends on `Protocol`s in `app/core/interfaces/ports.py`, never on
  FastAPI, SQLAlchemy, ROS or a model runtime.
- **Rationale:** The rules that decide whether a student is marked present must
  be testable in microseconds with no database, no model weights and no GPU.
  That is what makes a full CI run on CPU possible, and it is what makes the
  identity engine's behaviour auditable.
- **Consequences:**
  - Every port has at least two implementations: real and fake.
  - Route handlers become thin adapters (parse -> call core -> serialise).
  - The edge ROS code cannot import the cloud core directly (different Python),
    so the shared logic is duplicated deliberately rather than via a package
    dependency. The duplication is small and is checked by a parity test.
- **Rejected:** shared `common/` package installed into both — a single wheel
  across Python 3.12 and 3.13 plus a ROS build was more friction than the few
  duplicated pure functions were worth.
