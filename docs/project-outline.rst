Project Outline
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