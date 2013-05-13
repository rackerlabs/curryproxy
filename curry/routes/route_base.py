import abc


class RouteBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def match(self, request_url):
        raise NotImplementedError

    @abc.abstractmethod
    def issue_request(self, request):
        raise NotImplementedError
