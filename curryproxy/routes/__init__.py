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
from curryproxy.routes import endpoints_route
from curryproxy.routes import forwarding_route
from curryproxy.routes import status_route

# Hoist classes into the package namespace
EndpointsRoute = endpoints_route.EndpointsRoute
ForwardingRoute = forwarding_route.ForwardingRoute
StatusRoute = status_route.StatusRoute
