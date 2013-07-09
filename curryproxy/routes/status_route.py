"""The classes in this module have been lifted into the package namespace.

Classes:
    StatusRoute: Route to check the status of CurryProxy.

"""
from curryproxy.responses import StatusResponse
from curryproxy.routes.route_base import RouteBase


class StatusRoute(RouteBase):
    """Route to check the status of CurryProxy.

    This unique route doesn't communicate with any backend endpoints and can be
    used to determine CurryProxy's status even if the endpoints CurryProxy is
    configured to communicate with are malfunctioning or unresponsive.

    """
    def __init__(self, url_patterns):
        """Initialize a new StatusRoute.

        Args:
            url_patterns: List of URL patterns which this route will handle.
                Incoming requests must begin with one of these patterns for
                this route to handle the request.

        """
        self._url_patterns = url_patterns

    def __call__(self, request):
        return StatusResponse(request).response

    def _find_pattern_for_request(self, request_url):
        if request_url in self._url_patterns:
            return True

        return None
