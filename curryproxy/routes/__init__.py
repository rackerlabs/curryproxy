from curryproxy.routes import endpoints_route
from curryproxy.routes import forwarding_route

# Hoist classes into the package namespace
EndpointsRoute = endpoints_route.EndpointsRoute
ForwardingRoute = forwarding_route.ForwardingRoute
