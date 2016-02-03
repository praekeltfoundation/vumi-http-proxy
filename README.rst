vumi-http-proxy
====

Black & White listing HTTP Proxy for Vumi Sandbox HTTP requests

|vumi-proxy-ci| |vumi-proxy-cover|

.. |vumi-proxy-ci| image:: https://travis-ci.org/praekelt/vumi-http-proxy.svg?branch=develop
    :alt: Vumi-http-proxy Travis CI build status
    :scale: 100%
    :target: https://travis-ci.org/praekelt/vumi-http-proxy

.. |vumi-proxy-cover| image:: https://coveralls.io/repos/github/praekelt/vumi-http-proxy/badge.svg?branch=develop
    :alt: Vumi-http-proxy coverage on Coveralls
    :scale: 100%
    :target: https://coveralls.io/r/praekelt/vumi-http-proxy?branch=develop

To build this locally::

	$ virtualenv ve
	$ source ve/bin/activate
	(ve)$ pip install -e .
	(ve)$ twistd -n vumi_http_proxy --interface=IPADDRESS --port=PORTNO

Alternatively::

	$ virtualenv ve
	$ source ve/bin/activate
	(ve)$ pip install -e .
	(ve)$ clickme --interface IPADDRESS --port PORTNO



	