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


class ConfigLoader(object):
    """ Function lookalike that loads config files

    Hides the details of looking for and loading a file from the
    caller.
    """
    def __init__(self):
        self.formats = {".yaml": yaml.safe_load,
                        ".json": json.load,
                        ".ini": self.confparserloader,
                        ".conf": self.logconfloader}

    @staticmethod
    def confparserloader(f):
        """ For now this returns a configparser

        FIXME: should unpack the data in the configparser into a dict or
        dict-like object (or does configparser already work that way?
        I'm not sure.
        """

        cp = ConfigParser()
        cp.readfp(f)
        return cp

    @staticmethod
    def logconfloader(f):
        """ Load logging.conf files

        This one doesn't return anything and shouldn't need to. It just
        passes the file to logging.fileConfig()
        """
        # Doesn't return data. Shouldn't need to.
        logging.config.fileConfig(f)

    def __call__(self, path):
        return self._load(path)

    def _load(self, path):
        """ Load a data structure from a file path

        Args:
            filename: The file to load

        Returns:
            Whatever data structure is in the file.

        Supports yaml, json, and configparser files, detecting file type
        by extension.  Others can be added easily enough.

        Callers can query Loader.formats for a list of known formats.
        """
        ext = os.path.splitext(path)[1]
        loaders = self.formats
        if ext not in loaders:
            msg = "Don't know how to load {}. Supported filetypes: {}"
            filetypes = ", ".join(loaders.keys())
            raise ValueError(msg.format(path, filetypes))
        loader = loaders[ext]

        with open(path) as f:
            try:
                logging.debug("Loading %s using %s", path, loader)
                return loader(f)
            except (ValueError, yaml.YAMLError) as e:
                # Different loaders can raise different error types on bad
                # data. Turn them into ConfigErrors so callers don't need to
                # depend on loader internals to catch the exceptions.
                msg = "Problem loading file: {}. The error was: {}"
                msg = msg.format(path, str(e))
                raise ConfigError(msg)

    def search(self, name, directory, loaders=None):
        """ Look for a config file of any supported type

        name -- The root name of the file you're looking for
        directory -- The directory to look in
        loaders -- a extension-to-loader dictionary

        You can use *loaders* to pass a custom loader for a given
        extension.
        """

        logging.debug("searching for %s in `%s`", name, directory)
        for ext in self.formats:
            path = os.path.join(directory, name) + ext
            logging.debug("trying: " + path)
            try:
                data = self._load(path)
                logging.debug("found %s at %s", name, path)
                return data
            except IOError:
                pass

        # No file found
        msg = "Couldn't find '{}' under '{}' with any extension"
        logging.debug(msg)
        raise IOError(msg.format(name, directory))


load = ConfigLoader()
