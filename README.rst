CurryProxy
==========
A fast and performant proxy and aggregator for querying multiple instances of an API spread across globally distributed data centers.

.. image:: https://travis-ci.org/rackerlabs/curryproxy.png
         :target: https://travis-ci.org/rackerlabs/curryproxy

Capabilities
------------
- CurryProxy can handle multiple `routes <https://github.com/rackerlabs/curryproxy/wiki/Routes>`_ for use against different revisions of an API or for use against completely unrelated APIs. See `etc/routes.sample.json <https://github.com/rackerlabs/curryproxy/blob/master/etc/routes.sample.json>`_ for an example configuration.

- Simple request forwarding (useful for preserving backwards compatability with pre-CurryProxy versions of an API hosted in a single datacenter)

  - Example: ``GET https://api.example.com/v1.0/foo/bar`` forwarded to ``GET https://1.api.example.com/v1.0/foo/bar``

- Advanced request forwarding to multiple endpoints

  - Example: ``GET https://api.example.com/1,2/v1.0/foo/bar`` forwarded to the following:
  
    - ``GET https://1.api.example.com/v1.0/foo/bar``
        
    - ``GET https://2.api.example.com/v1.0/foo/bar``
        
  - Requests are made in parallel
    
  - JSON responses received from multiple endpoints are `aggregated <https://github.com/rackerlabs/curryproxy/wiki/Multiple-Endpoints-Aggregation>`_ and returned to the client
    
    - Example: ``{"foo": 1}`` received from 1 and ``{"bar": 2}`` received from 2 are aggregated to ``[{"foo": 1}, {"bar": 2}]`` and returned to the client
        
  - Rich, meaningful `errors <https://github.com/rackerlabs/curryproxy/wiki/Multiple-Endpoints-Aggregation#error-handling>`_ logged *and* returned to the client when a proxied request fails

Installation
------------
- ``pip install curryproxy``
- `Setup <https://github.com/rackerlabs/curryproxy/wiki/Setup>`_ the configuration files and start it up!

Limitations
-----------
- Merging responses from multiple endpoints together occurs only under certain conditions outlined on the `Multiple Endpoints Aggregation <https://github.com/rackerlabs/curryproxy/wiki/Multiple-Endpoints-Aggregation>`_ wiki page.

Roadmap
-------
- OData support for server-side ordering and paging
- Response caching for a specified time
