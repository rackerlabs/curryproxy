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
"""Routes used to forward incoming requests to destination endpoints.

Modules:
    route_base: Base class for routes.
    route_factory: Produces routes based on information found in a
        configuration file.

Classes:
    EndpointsRoute: Handles forwarding a request to multiple backend endpoints.
    ForwardingRoute: Direct communication with a single endpoint.
    StatusRoute: Route to check the status of CurryProxy.

"""
# Not sure if these are still necessary
from curryproxy.routes.endpoints_route import EndpointsRoute
from curryproxy.routes.forwarding_route import ForwardingRoute
from curryproxy.routes.status_route import StatusRoute

# The only config functions callers should ever need.
from curryproxy.helpers import load
from .config import make

# Get lint to shut up.
__all__ = ['EndpointsRoute', 'ForwardingRoute', 'StatusRoute', 'make', 'load']
