# Copyright (c) 2013 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Contains a base class for routes.

Classes:
    RouteBase: Base class for routes in CurryProxy.

"""
import abc


class RouteBase(object):
    """Base class for routes in CurryProxy."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(self, request):
        """Handles an incoming request to this route.

        It is safe to assume match(request_url) has already been called and the
        incoming request has been matched to this route. Construct and return
        a response based on the incoming request.

        Args:
            request: A webob.Request instance representing the incoming
                request.
        Returns:
            A webob.Response instance to be returned to the requestor.

        """
        raise NotImplementedError

    def match(self, request_url):
        """Determines if this route can handle the incoming request_url.

        Args:
            request_url: URL of the incoming request.

        Returns:
            True if this route can handle the incoming request. Otherwise,
            False.

        """
        url_pattern = self._find_pattern_for_request(request_url)
        if url_pattern is not None:
            return True

        return False

    @abc.abstractmethod
    def _find_pattern_for_request(self, request_url):
        """Finds the route's URL pattern to match the incoming request.

        Compare the incoming request_url to the URL patterns this route serves
        to determine which URL pattern matches the request.

        Args:
            request_url: URL of the incoming request.
        Returns:
            URL pattern string matching the incoming request if one exists.
                Otherwise, return None.

        """
        raise NotImplementedError
