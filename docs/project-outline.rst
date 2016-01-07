Black & White-listing HTTP Proxy
================================

Vumi Go, the hosted Vumi environment, while being horizontally scalable and
consisting of a number of moving parts over time grew to be more monolithic than
originally designed. We are in the process of breaking off different chunks and
housing these in separate micro-services. The idea of micro-services is to make
a single bit of server software responsible for a single task instead of
everything being inlined in the main application. These micro-services interact
with the wider system through a number of APIs and as a result should draw
clearer lines of separation & responsibility between the various moving parts of
a large application. The idea behind micro-services is also that they would
allow for the internals to be more easily refactored and supported by specific
teams.

All of our micro-services that we are running or are designing expose HTTP APIs.
Generally they accept and respond with JSON payloads. These services need to be
isolated from other applications. For obvious reasons we cannot allow rogue
applications access internal APIs.

Vumi’s Javascript sandbox allows application developers to access HTTP
resources, we need a proxy that intercepts these outbound HTTP calls and checks
whether the calls to the specified resources are allowed or not. This boils down
to maintaining a blacklist of disallowed HTTP resources and per request checking
against the blacklist.

People to poke: Simon de Haan (smn), Simon Cross (hodgestar), Justin van der
Merwe (justinvdm), Jeremy Thurgood (jerith)


Useful links
------------

* `Twisted from Scratch <https://twistedmatrix.com/documents/current/core/howto/tutorial/index.html>`_
* `Introduction to Deferreds <https://twistedmatrix.com/documents/current/core/howto/defer-intro.html>`_
* `Deferred Reference <https://twistedmatrix.com/documents/current/core/howto/defer.html>`_
* `Getting Connected with Endpoints <https://twistedmatrix.com/documents/current/core/howto/endpoints.html>`_
* `Python Documentation <https://docs.python.org/2/index.html>`_
* `Twisted's simple built-in HTTP proxy <https://twistedmatrix.com/documents/current/api/twisted.web.proxy.html>`_
* `Wikipedia overview of the HTTP protocol <https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol>`_
