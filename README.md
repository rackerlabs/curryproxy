Curry (v0.1)
=============

A fast and performant proxy and a result aggregator written in C# using TPL. Has Caching and Pagination support.

What this version does?
----------------------
 
 --  Relays request to a another URL and forwards the response.  Forwarding happens based on a key in the original Uri.
 
		Example: GET  https://api.drivesrvr.com/dfw/v1.0/user/agents   gets forwarded to https://dfw.api.drivesrvr.com/v1.0/user/agents
 
-- For requests that require multiple forwarding, Curry forwards these requests in Parallel using C# TPL. Curry also aggregates these results.
Curry blocks until it has received responses from all endpoints.
 
		Example: GET https://api.drivesrvr.com/dfw,ord,syd/v1.0/user/agents gets forwarded as three different requests as below.
		       
		{
		        https://dfw.api.drivesrvr.com/v1.0/user/agents
		        https://ord.api.drivesrvr.com/v1.0/user/agents
		        https://syd.api.drivesrvr.com/v1.0/user/agents
		}     
 
Has a basic prototype of multiple requests and aggregating results working - work in progress.
 
-- Configuration to set up Forwarding Uri.

-- Caches the response for 30 seconds.
 
