Curry [![Build Status](https://travis-ci.org/rackerlabs/curryproxy.png)](https://travis-ci.org/rackerlabs/curryproxy)
=====
A fast and performant proxy and aggregator for querying multiple instances of an API spread across globally distributed data centers.

Initial Capabilities
--------------------
- Definition of multiple routes for Curry to handle (see `etc/routes.sample.json`)
- Simple request forwarding (useful for backwards compatability with pre-Curry versions of an API hosted in a single datacenter)
	- Example: `GET https://api.example.com/v1.0/foo/bar` forwarded to `GET https://atl.api.example.com/v1.0/foo/bar`
- Advanced request forwarding to multiple datacenters
	- Example: `GET https://api.example.com/atl,sat/v1.0/foo/bar` forwarded to the following:
		- `GET https://atl.api.example.com/v1.0/foo/bar`
		- `GET https://sat.api.example.com/v1.0/foo/bar`
	- Requests are made in parallel
	- JSON responses received from multiple endpoints are aggregated and returned to the client
		- Example: `{"foo": 1}` received from ATL and `{"bar": 2}` received from SAT are aggregated to `[{"foo": 1}, {"bar": 2}]` and returned to the client. **Note:** The client is currently responsible for ordering the results. See [Roadmap](#roadmap) for future improvements.
	- Rich, meaningful errors logged *and* returned to the client when a proxied request fails

Caveats
-------
- Only JSON responses can be aggregated
- TODO: Determine which responses are aggregated. Currently, only GET requests resulting in responses with `200` response codes and `Content-Type: application/json` headers are aggregated.

Setup
-----
- https://github.com/racker/Curry/wiki/Setup

<a id="roadmap"></a>Roadmap
-------
- OData support for server-side ordering and paging
- Response caching for a specified time

Contributing
------------

Run basic code quality tests before submitting a code contribution:

```
tox -e flake8
tox -e py27
tox -e py33
tox -e pylint-errors
```

Thanks!
