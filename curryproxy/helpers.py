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
"""Helper classes and functions used throughout CurryProxy.

Classes:
    ReprString: A str subclass overriding the __repr__ function.

Functions:
    exception_wrapper: Function wrapper that logs any exception in the wrapped
        function.
    profile_wrapper: Function wrapper that logs a profiled report of the
        wrapped function.
    intrange: Turn a string representing an integer range (e.g. 5-100)
        into the corresponding list of ints.

Attributes:
    ENVIRON_REQUEST_UUID_KEY: Key name to be used to uniquely identify a
        request in PEP 333's WSGI environ dictionary.
    LOGGING_LEVEL_DEBUG: Integer representation of the DEBUG logging level as
        outlined at http://docs.python.org/2/howto/logging.html#logging-levels.

"""
import os
import cProfile
import logging
import pstats
import StringIO
import uuid
import json
from ConfigParser import ConfigParser

import yaml

from curryproxy.errors import ConfigError


ENVIRON_REQUEST_UUID_KEY = 'curryproxy.request_uuid'
LOGGING_LEVEL_DEBUG = 10


class ReprString(str):
    """A str subclass overriding the __repr__ function."""
    def __repr__(self):
        """Returns the real string instead of the __repr__ representation"""
        return self


def exception_wrapper(function):
    """Function wrapper that logs any exception in the wrapped function.

    Args:
        function: The function to be wrapped.

    Returns:
        A wrapped function.

    """
    def wrapper(*args, **kwargs):
        """Logs any exception in the called function."""
        request_uuid = ReprString(uuid.uuid4())

        try:
            wsgi_environ = args[1]
            wsgi_environ[ENVIRON_REQUEST_UUID_KEY] = request_uuid

            return function(*args, **kwargs)
        except Exception as exception:
            logging.exception(exception, extra={'request_uuid': request_uuid})

    return wrapper


def profile_wrapper(function):
    """Function wrapper that logs a profiled report of the wrapped function.

    Args:
        function: The function to be wrapped.

    Returns:
        A wrapped function.

    """
    def wrapper(*args, **kwargs):
        """Logs a profiled report in the called function."""
        logging_level = logging.getLogger().getEffectiveLevel()
        if logging_level > LOGGING_LEVEL_DEBUG:
            return function(*args, **kwargs)

        profile = cProfile.Profile(builtins=False)
        profile.enable()

        function_result = function(*args, **kwargs)

        profile.disable()

        stream = StringIO.StringIO()
        stats = pstats.Stats(profile, stream=stream)
        stats.sort_stats('time')
        stats.print_stats()

        stream.seek(0)
        short_msg = stream.readline()
        stats_string = stream.getvalue()

        wsgi_environ = args[1]
        request_uuid = wsgi_environ[ENVIRON_REQUEST_UUID_KEY]
        logging.debug(short_msg.strip(),
                      extra={'cprofile_stats': ReprString(stats_string),
                             'request_uuid': request_uuid})

        return function_result

    return wrapper


def intrange(rangespec):
    """ Convert a string representing an integer range into a list of ints.

    Args:
        rangespec: A string representing an integer or range of
            integers, e.g. "13" or "37-42".

    Returns:
        A list of integers within the range, inclusive.
    """

    # Do we really need all this extra checking just to stop the admin
    # from doing something stupid in the conf file?
    if isinstance(rangespec, int):
        return [rangespec]
    elif '-' not in rangespec:
        return [int(rangespec)]
    elif rangespec.count('-') > 1:
        msg = "`%s` is neither an integer nor an integer range"
        raise ValueError(msg, rangespec)
    else:
        first, last = rangespec.split('-')
        first, last = int(first), int(last)
        if first > last:
            msg = "range `%s` stops before it starts"
            raise ValueError(msg, rangespec)
        return range(first, last+1)


def load(path):
    """ Load a YAML config file """

    logging.debug("Loading file: %s", path)
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        # Turn these into ConfigErrors so callers don't need to
        # depend on loader internals to catch the exceptions
        raise ConfigError(str(e))

def init_log(path):
    """ Set up logging """
    try:
        conf = load(path)
    except IOError:
        # This could be intentional (e.g. no log file provided), so don't
        # worry about it. But do note it.
        logging.warning("Couldn't load logging configuration from %s", path)
        logging.warning("Python logging defaults will be used")
    except Exception as e:
        # Something else went wrong -- something unexpected. Most likely
        # cause is a malformed yaml file. Better crash so it's obvious.
        logging.error("Problem with log configuration: %s", e)
        raise
    else:
        logging.config.dictConfig(conf)

    logging.info("Logging initialized from %s", path)
    logging.error("[ERROR MESSAGE TEST]")
    logging.warn("[WARNING MESSAGE TEST]")
    logging.info("[INFO MESSAGE TEST]")
    logging.debug("[DEBUG MESSAGE TEST]")
