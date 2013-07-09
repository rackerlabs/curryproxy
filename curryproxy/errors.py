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
"""Error classes to represent both server- and client-side errors.

Exceptions:
    ConfigError: An error representing an invalid configuration.
    RequestError: Represents an error with an incoming request.

"""


class ConfigError(Exception):
    """An error representing an invalid configuration."""
    pass


class RequestError(Exception):
    """Represents an error with an incoming request."""
    pass
