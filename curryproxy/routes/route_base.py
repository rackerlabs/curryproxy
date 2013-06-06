import abc


class RouteBase(object):
    __metaclass__ = abc.ABCMeta

    def match(self, request_url):
        url_pattern = self._find_pattern_for_request(request_url)
        if url_pattern is not None:
            return True

        return False

    @abc.abstractmethod
    def _find_pattern_for_request(self, request_url):
        """Determines if the route matches the incoming request

        Compare the incoming request_url to the url_patterns this route serves
        to determine whether or not the route matches the incoming request.

        Args:
            request_url: URL of the incoming request
        Returns"
            True if this route can server the incoming request. Otherwise,
            false.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def issue_request(self, request):
        raise NotImplementedError
