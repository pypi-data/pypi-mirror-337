import pytest
from syrupy import matchers

from matomo_core.core import MatomoCore


def make_matcher():  # noqa: ANN201
    return matchers.path_type({"gt_ms": (float,), "rand": (int,)})


def make_state_matcher():  # noqa: ANN201
    return matchers.path_type({"start_ns": (int,), "rand": (int,)})


def test_empty_matomo_url_raise_value_error(snapshot) -> None:  # noqa: ANN001
    with pytest.raises(ValueError) as exc:
        MatomoCore(matomo_url="", id_site=1)
    assert str(exc) == snapshot


def test_empty_idsite_raise_value_error(snapshot) -> None:  # noqa: ANN001
    mc = MatomoCore(matomo_url="https://example.com")
    with pytest.raises(ValueError) as exc:
        mc.build_tracking_state(
            user_agent="ua",
            request_path="/example",
            request_url="https://example.com/example",
            request_url_rule="/example",
            method="GET",
            remote_addr="127.0.0.1",
        )
    assert str(exc) == snapshot


def test_matomo_core_doesnt_track_ignored_path(snapshot_json) -> None:  # noqa: ANN001
    mc = MatomoCore(matomo_url="https://example.com", id_site="3", ignored_routes=["/ignored"])

    tracking_state = mc.build_tracking_state(
        method="GET",
        remote_addr="127.0.0.1",
        user_agent="ua",
        request_path="/ignored",
        request_url="https://example.com/example",
        request_url_rule="/ignored",
    )
    assert tracking_state["tracking"] is False
    assert tracking_state == snapshot_json(matcher=make_state_matcher())
