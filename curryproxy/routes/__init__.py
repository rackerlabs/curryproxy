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
