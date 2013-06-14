import abc


class RouteBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(self, request):
        """Handles an incoming request to this route

        It is safe to assume match(request_url) has already been called and the
        incoming request has been matched to this route. Construct and return
        a response based on the incoming request.

        Args:
            request: A webob.Request instance representing the incoming request
        Returns:
            A webob.Response instance to be returned to the requestor.

        """
        raise NotImplementedError

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
        Returns:
            True if this route can server the incoming request. Otherwise,
            false.
        """
        raise NotImplementedError
