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
"""A proxy and aggregator for multiple instances of an API.

Packages:
    responses: Response classes to help form a response for the client.
    routes: Route classes to forward incoming requests from a client to the
        destination endpoints.
    tests: Tests.
Modules:
    errors: Error classes to represent both server- and client-side errors.
    helpers: Small helper functions for CurryProxy.
Classes:
    CurryProxy: WSGI callable responsible for handling requests and returning
        responses.

"""
from curryproxy import server

# Hoist class into the package namespace
CurryProxy = server.CurryProxy
