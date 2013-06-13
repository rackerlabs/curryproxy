from curryproxy.responses import StatusResponse
from curryproxy.routes.route_base import RouteBase


class StatusRoute(RouteBase):
    def __init__(self, url_patterns):
        self._url_patterns = url_patterns

    def _find_pattern_for_request(self, request_url):
        if request_url in self._url_patterns:
            return True

        return None

    def issue_request(self, request):
        return StatusResponse(request).response
