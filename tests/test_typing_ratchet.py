"""Type-debt ratchet.

The pre-W1 modules were written without type hints. W3 restructures them. Until
then ``mypy app`` reports a known, fixed number of errors — and this test fails
if that number goes **up**, so the debt cannot silently grow.

If you fix some errors, lower ``MAX_LEGACY_ERRORS`` in this file to the new
count. That is the intended workflow: the ratchet only tightens.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

#: MEASURED 2026-09-29 by `.venv/bin/mypy app`. Lower this, never raise it.
MAX_LEGACY_ERRORS = 32

#: Modules written in W1+ that must be completely clean.
STRICT_TARGETS = [
    "app/core",
    "app/registry",
    "app/observability",
    "app/retention.py",
    "app/cli.py",
    "app/models",
]


def _run_mypy(*targets: str) -> subprocess.CompletedProcess[str]:
    """Invoke mypy and return the completed process."""
    return subprocess.run(
        [sys.executable, "-m", "mypy", *targets],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def _error_lines(output: str) -> list[str]:
    """Return only the ``path:line: error: ...`` lines, ignoring notes."""
    return [line for line in output.splitlines() if ": error:" in line]


def _error_count(output: str) -> int:
    """Extract the error total from mypy's final summary line."""
    for line in reversed(output.strip().splitlines()):
        if "Found " in line and "error" in line:
            for token in line.replace(":", " ").split():
                if token.isdigit():
                    return int(token)
    return 0


@pytest.mark.slow
def test_strict_modules_have_no_type_errors() -> None:
    """New code is held to the strict settings with no exceptions.

    mypy follows imports, so checking ``app/core`` also pulls in legacy modules
    transitively. We therefore assert on the errors *located in* the strict
    files, not on mypy's exit code.
    """
    result = _run_mypy(*STRICT_TARGETS)
    strict_paths = tuple(f"{target}/" if not target.endswith(".py") else target for target in STRICT_TARGETS)
    offending = [
        line for line in _error_lines(result.stdout) if any(line.startswith(path) for path in strict_paths)
    ]
    assert not offending, "type errors in W1+ modules (which must be clean):\n" + "\n".join(offending)


@pytest.mark.slow
def test_legacy_type_debt_does_not_grow() -> None:
    """The legacy error count may only go down."""
    result = _run_mypy("app")
    count = _error_count(result.stdout)
    assert count <= MAX_LEGACY_ERRORS, (
        f"legacy type debt grew: {count} errors, budget is {MAX_LEGACY_ERRORS}.\n"
        f"{result.stdout}\n"
        "Either fix the errors, or (if they are legitimate) raise "
        "MAX_LEGACY_ERRORS deliberately. Never do the latter silently."
    )


@pytest.mark.slow
def test_all_remaining_type_errors_are_in_legacy_modules() -> None:
    """Pin the debt to specific files so W3 knows exactly what to fix.

    This is the explicit backlog. When W3 lands, this list must shrink.
    """
    result = _run_mypy("app")
    allowed = {"app/api/routes.py", "app/main.py", "app/services/", "app/pipeline/"}
    offenders = {
        line.split(":", 1)[0]
        for line in _error_lines(result.stdout)
        if not any(line.startswith(path) for path in allowed)
    }
    assert not offenders, (
        "type errors outside the known legacy backlog: "
        f"{sorted(offenders)}. Fix these or add them to the backlog deliberately."
    )


@pytest.mark.slow
def test_no_module_uses_the_builtin_any_as_a_type() -> None:
    """``-> tuple[bool, any, str]`` type-checks as ``Any`` and documents nothing."""
    result = _run_mypy("app")
    offenders = [line for line in result.stdout.splitlines() if "builtins.any" in line]
    assert not offenders, "builtin `any` used as a type annotation:\n" + "\n".join(offenders)
