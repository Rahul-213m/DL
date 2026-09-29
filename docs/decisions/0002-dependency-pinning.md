# ADR 0002 — Exact dependency pins, no ranges

- **Status:** Accepted
- **Context:** The legacy `requirements.txt` used `>=` floors
  (`insightface>=0.7.3`) while the machine had `1.0.1` installed. Nothing
  recorded which version the tests actually pass against, and `insightface` is
  exactly the kind of package where a minor bump changes model behaviour.
- **Decision:** Exact pins (`==`) in `pyproject.toml`, mirrored into
  `requirements.txt`, derived from `pip freeze` on the dev machine. Every pin
  carries a comment recording the machine it was measured on.
- **Rationale:** Face recognition is unforgiving of silent version drift. A
  reproducible environment is worth more than automatic upgrades; upgrades
  become a deliberate, tested commit.
- **Consequences:** Security updates are manual. Accepted; the upgrade path is
  a PR that runs the full evaluation harness first.
- **Rejected:** compatible-release (`~=`) — still allows drift within a minor.
