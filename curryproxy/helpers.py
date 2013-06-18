import cProfile
import logging
import pstats
import StringIO
import uuid


ENVIRON_REQUEST_UUID_KEY = 'curryproxy.request_uuid'
# http://docs.python.org/2/howto/logging.html#logging-levels
LOGGING_LEVEL_DEBUG = 10


class ReprString(str):
    def __repr__(self):
        return self


def exception_wrapper(function):
    def wrapper(*args, **kwargs):
        request_uuid = ReprString(uuid.uuid4())

        try:
            wsgi_environ = args[1]
            wsgi_environ[ENVIRON_REQUEST_UUID_KEY] = request_uuid

            return function(*args, **kwargs)
        except Exception as e:
            logging.exception(e, extra={'request_uuid': request_uuid})

    return wrapper


def profile_wrapper(function):
    def wrapper(*args, **kwargs):
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
