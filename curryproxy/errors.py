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
