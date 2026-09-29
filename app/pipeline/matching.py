from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class MatchResult:
    roll_no: str | None
    score: float
    route: str  # auto, confirm, review


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a, b = np.asarray(a, dtype=np.float32), np.asarray(b, dtype=np.float32)
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    return float(np.dot(a, b) / denom) if denom else 0.0


def route_match(roll_no: str | None, score: float, high: float, low: float) -> MatchResult:
    if roll_no is not None and score >= high:
        return MatchResult(roll_no, score, "auto")
    if roll_no is not None and score >= low:
        return MatchResult(roll_no, score, "confirm")
    return MatchResult(None, score, "review")
