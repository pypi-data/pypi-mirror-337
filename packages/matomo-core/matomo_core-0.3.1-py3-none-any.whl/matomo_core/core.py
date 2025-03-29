"""The Flask middleware for Matomo tracking."""

import json
import logging
import random
import re
import time
import typing as t

import typing_extensions as t_ext  # Needed for NotRequired for Python < 3.11

import matomo_core.constants

logger = logging.getLogger("flask_matomo2")


DEFAULT_HTTP_TIMEOUT: int = 5


class MatomoTrackingState(t_ext.TypedDict):
    """Tracking state for Matomo."""

    tracking: bool
    start_ns: float
    tracking_data: dict[str, t.Any]
    custom_tracking_data: t_ext.NotRequired[dict[str, t.Any]]


class MatomoCore:
    """The Matomo object provides the central interface for interacting with Matomo."""

    def __init__(
        self,
        *,
        matomo_url: str,
        id_site: t.Optional[t.Union[str, int]] = None,
        token_auth: t.Optional[str] = None,
        base_url: t.Optional[str] = None,
        ignored_routes: t.Optional[list[str]] = None,
        routes_details: t.Optional[dict[str, dict[str, str]]] = None,
        ignored_patterns: t.Optional[list[str]] = None,
        ignored_ua_patterns: t.Optional[list[str]] = None,
        allowed_methods: t.Union[list[str], t.Literal["all-methods"]] = "all-methods",
        ignored_methods: t.Optional[list[str]] = None,
    ) -> None:
        """Matamo tracker plugin.

        Observe that `http_timeout` is ignored if you provide your own http client.

        Args:
            matomo_url: url to Matomo installation
            id_site: id of the site that should be tracked on Matomo
            token_auth: token that can be found in the area API in the settings of Matomo
            base_url: base_url to the site that should be tracked. Default: None.
            ignored_routes: a list of routes to ignore
            routes_details: a dict of details for routes. Default: None.
            ignored_patterns: list of regexes of routes to ignore. Default: None.
            ignored_ua_patterns: list of regexes of User-Agent to ignore requests. Default: None.
            allowed_methods: list of methods to track or "all-methods". Default: "all-methods".
            ignored_methods: list of methods to ignore, takes precedence over allowed methods. Default: None.
        """
        if not matomo_url:
            raise ValueError("matomo_url has to be set")

        # Allow backend url with or without the filename part and/or trailing slash
        self.matomo_url = (
            matomo_url if matomo_url.endswith(("/matomo.php", "/piwik.php")) else matomo_url.strip("/") + "/matomo.php"
        )
        self.id_site = id_site
        self.token_auth = token_auth
        self.base_url = base_url.strip("/") if base_url else base_url
        self.ignored_ua_patterns = []
        if ignored_ua_patterns:
            self.ignored_ua_patterns = [re.compile(pattern) for pattern in ignored_ua_patterns]
        self.ignored_routes: list[str] = ignored_routes or []
        self.routes_details: dict[str, dict[str, str]] = routes_details or {}
        self.ignored_patterns = []
        if ignored_patterns:
            self.ignored_patterns = [re.compile(pattern) for pattern in ignored_patterns]

        self.allowed_methods: set[str] = set()
        if allowed_methods == "all-methods":
            self.allowed_methods = matomo_core.constants.HTTP_METHODS
        elif allowed_methods:
            self.allowed_methods.update(method.upper() for method in allowed_methods)

        self.ignored_methods: set[str] = {method.upper() for method in ignored_methods} if ignored_methods else set()
        if not self.token_auth:
            logger.warning("'token_auth' not given, NOT tracking ip-address")

    def should_request_be_ignored(self, *, url_rule: str, method: str, user_agent: str) -> bool:
        """Check if this request should be ignored.

        Args:
            url_rule: the relative url for this request
            method: the http method use for this request
            user_agent: the user-agent for this request
        """
        if url_rule in self.ignored_routes:
            return True
        if method in self.ignored_methods or method not in self.allowed_methods:
            return True
        if any(ua_pattern.match(user_agent) for ua_pattern in self.ignored_ua_patterns):
            return True
        return bool(any(pattern.match(url_rule) for pattern in self.ignored_patterns))

    def build_tracking_state(
        self,
        *,
        user_agent: str,
        request_path: str,
        request_url: str,
        method: str,
        remote_addr: t.Optional[str],
        request_url_rule: str = "",
        referrer: t.Optional[str] = None,
        forwarded_for: t.Optional[str] = None,
        lang: t.Optional[str] = None,
    ) -> MatomoTrackingState:
        """Build tracking state.

        Args:
            user_agent: the user-agent used for this request
            request_path: the path used for this request
            request_url: the url used for this request
            request_url_rule: the url_rule used for this request
            method: the HTTP method used for this request
            remote_addr: the remote address for this request
            forwarded_for: optional address from HTTP_X_FORWARDED_FOR setting
            referrer: optional url that is set as referrer
            lang: optional setting of used languages
        """
        if not self.id_site:
            raise ValueError("id_site has to be set")

        if self.should_request_be_ignored(url_rule=request_url_rule, method=method, user_agent=user_agent):
            return {"tracking": False, "start_ns": time.perf_counter_ns(), "tracking_data": {}}
        url = self.base_url + request_path if self.base_url else request_url
        action_name = request_url_rule or "Not Found"
        data = {
            # site data
            "idsite": str(self.id_site),
            "rec": "1",
            "apiv": "1",
            "send_image": "0",
            # request data
            "ua": user_agent,
            "action_name": action_name,
            "url": url,
            # "_id": id,
            "cvar": {
                "http_status_code": None,
                "http_method": method,
            },
            # random data
            "rand": random.getrandbits(32),
        }
        if self.token_auth:
            ip_address = forwarded_for or remote_addr
            data["token_auth"] = self.token_auth
            if ip_address:
                data["cip"] = ip_address

        if lang:
            data["lang"] = lang

        if referrer:
            data["urlref"] = referrer

        # Overwrite action_name, if it was configured with details()
        if self.routes_details.get(action_name):
            data.update(self.routes_details[action_name])

        return {
            "tracking": True,
            "start_ns": time.perf_counter_ns(),
            "tracking_data": data,
        }

    @classmethod
    def track_request_end(cls, status_code: int, tracking_state: MatomoTrackingState) -> None:
        """Finish tracking.

        Args:
            status_code: the status_code for this request
            tracking_state: the state for this request
        """
        if not tracking_state["tracking"]:
            return

        end_ns = time.perf_counter_ns()
        gt_ms = (end_ns - tracking_state["start_ns"]) / 1000
        tracking_state["tracking_data"]["gt_ms"] = gt_ms
        tracking_state["tracking_data"]["cvar"]["http_status_code"] = status_code

    @classmethod
    def prepare_tracking_data_for_matomo(
        cls, tracking_state: MatomoTrackingState, exc: t.Optional[BaseException] = None
    ) -> t.Optional[dict[str, t.Any]]:
        """Finish tracking and send to Matomo."""
        if not tracking_state["tracking"]:
            return None
        logger.debug("tracking_state=%s", tracking_state)
        tracking_data = tracking_state["tracking_data"]
        for key, value in tracking_state.get("custom_tracking_data", {}).items():
            if key == "cvar" and "cvar" in tracking_data:
                tracking_data["cvar"].update(value)
            else:
                tracking_data[key] = value
        if exc:
            tracking_data["ca"] = 1
            tracking_data["cra"] = repr(exc)

        if "cvar" in tracking_data:
            cvar = tracking_data.pop("cvar")
            tracking_data["cvar"] = json.dumps(cvar)

        return tracking_data
