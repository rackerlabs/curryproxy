Curry [![Build Status](https://jenkins.drivesrvr-dev.com/job/curry-master/badge/icon)](https://jenkins.drivesrvr-dev.com/job/curry-master/)
=====
A fast and performant proxy for querying multiple instances of an API spead across globally distributed datacenters.

Initial Capabilities
--------------------
- Definition of multiple routes for Curry to handle (see `etc/routes.sample.json`)
- Simple request forwarding (useful for pre-Curry versions of an API hosted in a single datacenter)
	- Example: `GET https://oldapi.olddomain.com/v1.0/foo/bar` forwarded to `GET https://api.rackspacecloud.com/v1.0/foo/bar`
- Advanced request forwarding to multiple datacenters
	- Example: `GET https://api.rackspacecloud.com/ord,syd/v2.0/foo/bar` forwarded to the following:
		- `GET https://ord.api.rackspacecloud.com/v2.0/foo/bar`
		- `GET https://syd.api.rackspacecloud.com/v2.0/foo/bar`
	- Requests are made in parallel
	- JSON responses received from multiple endpoints are aggregated and returned to the client
		- Example: `{"foo": 1}` received from ORD and `{"bar": 2}` received from SYD are aggregated to `[{"foo": 1}, {"bar": 2}]` and returned to the client. **Note:** The client is currently responsible for ordering the results. See [Roadmap](#roadmap) for future improvements.
	- Rich, meaningful errors logged *and* returned to the client when a proxied request fails

Caveats
-------
- Only JSON responses can be aggregated

<a id="roadmap"></a>Roadmap
-------
- OData support for server-side ordering and paging support
- Response caching for a specified time
