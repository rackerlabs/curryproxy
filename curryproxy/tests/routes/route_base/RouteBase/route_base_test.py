from curryproxy.routes.route_base import RouteBase


class RouteBaseTest(RouteBase):
    def __call__(self, request):
        super(RouteBaseTest, self).__call__(request)

    def _find_pattern_for_request(self, request_url):
        super(RouteBaseTest, self)._find_pattern_for_request(request_url)
