import numpy as np
from app.pipeline.matching import cosine_similarity, route_match

def test_cosine_and_threshold_routing():
    assert cosine_similarity(np.array([1, 0]), np.array([1, 0])) == 1.0
    assert route_match("R1", .8, .7, .4).route == "auto"
    assert route_match("R1", .5, .7, .4).route == "confirm"
    assert route_match("R1", .2, .7, .4).route == "review"


def test_score_below_conservative_auto_threshold_requires_review():
    # The observed R1→R3 false positive scored 0.632. It must not become
    # automatic attendance when HIGH is the production default of 0.70.
    assert route_match("R3", .632, .70, .35).route == "confirm"
