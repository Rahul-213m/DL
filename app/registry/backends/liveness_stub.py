"""Liveness / anti-spoof slot.

WHY THIS IS A STUB AND NOT A MODEL
----------------------------------
The brief lists an optional liveness check "to prevent photo-of-photo
attendance". That check does not exist in any permissively licensed model
today: the published anti-spoofing networks (Silent-Face, FAS) carry the same
licensing ambiguity as the recognition weights, and shipping a checker that
cannot actually detect a printed photo would be worse than shipping none,
because it converts an open question into a false assurance.

So this module provides the **wiring**, refuses to pretend, and fails loudly:

* :class:`UnsupportedLiveness` is what the registry hands back by default. It
  raises on every call, so a code path that depends on liveness cannot start
  silently in a deployment where it is not configured.
* :class:`LivenessStub` returns a neutral score and reports
  ``supported = False``. It exists so the pipeline, the configuration, the
  metrics and the tests can all exercise the *path* where liveness is
  consulted without pretending to check anything.
* The production guard (:meth:`app.core.config.Settings.validate_invariants`
  and the registry) **refuses** to run a deployment whose only liveness
  backend is a stub. A stub in production is a claim of protection that does
  not exist, and that is a compliance statement, not a configuration choice.

Swapping in a real checker is one class with three methods; see
``docs/model_licensing.md`` for the purchase options.
"""

from __future__ import annotations

import logging

import numpy as np

from app.core.domain.types import BBox

log = logging.getLogger(__name__)


class UnsupportedLiveness:
    """Placeholder used when no liveness backend is configured.

    Calling it is always a bug in the caller's control flow: the pipeline only
    consults liveness when the registry reports a supported checker.
    """

    #: Nothing is being checked.
    supported = False
    name = "unsupported"

    def warmup(self) -> None:
        """Nothing to load."""

    def check(self, image: np.ndarray, bbox: BBox) -> float:
        """Always raise: an unchecked face must never be scored as live."""
        del image, bbox
        raise RuntimeError(
            "no liveness backend is configured. Set LIVENESS_BACKEND to a real "
            "checker; the stub and the default are refused in production. "
            "See docs/model_licensing.md."
        )


class LivenessStub:
    """A liveness checker that checks nothing, and says so.

    Returns ``NEUTRAL_SCORE`` for every face. Used to exercise the code path
    where liveness is consulted (metrics, notes, event columns) without
    claiming any protection. ``supported`` is False, and the production guard
    reads it.
    """

    supported = False
    name = "liveness_stub"

    #: The score the stub reports. Deliberately mid-range: a low score would
    #: make every face look like a spoof, a high score would look like a pass,
    #: and both would be a fabricated result.
    NEUTRAL_SCORE = 0.5

    def warmup(self) -> None:
        """No weights to load."""

    def check(self, image: np.ndarray, bbox: BBox) -> float:
        """Return the neutral score without inspecting the image."""
        del image, bbox
        return self.NEUTRAL_SCORE


class NullLiveness:
    """Explicitly disabled checker: reports "live" and records nothing.

    Used when an operator has consciously accepted that this deployment does
    not perform spoof detection (the current state of every deployment). It is
    honest in both directions: the face is admitted to the queue, and the
    absence of a check is recorded on the attendance event.
    """

    supported = True
    name = "null"
    performs_check = False

    def warmup(self) -> None:
        """No weights to load."""

    def check(self, image: np.ndarray, bbox: BBox) -> float:
        """Report a full score, because no check was performed or refused."""
        del image, bbox
        return 1.0


__all__ = ["LivenessStub", "NullLiveness", "UnsupportedLiveness"]
