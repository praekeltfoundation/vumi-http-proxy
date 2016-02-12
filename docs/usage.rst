Twistd ServiceMaker Plugin Usage
================================

This plugin allows manual configuration of the HTTP Proxy.

First, build this locally::

	$ virtualenv ve
	$ source ve/bin/activate
	(ve)$ pip install -e .

To see list of all twistd plugins::

	(ve)$ twistd -d

In order to configure the proxy using default settings, a blacklist must be specified as follows::

	(ve)$ twistd -n vumi_http_proxy --blacklist=BLACKLISTFILENAME

This blacklist must be a PyYAML configuration file, an example of which can 
be found below (./docs/proxy_blacklist.yml):

.. literalinclude:: proxy_blacklist.yml
    :language: yaml

The default settings are::
	
	IP address: 0.0.0.0
	port: 8080
	blacklist: None

To run using manual configuration::

	(ve)$ twistd -n vumi_http_proxy --interface=IPADDRESS --port=PORTNO --blacklist=BLACKLISTFILENAME

For hints and a list of all available commands, please see::
	
	(ve)$ twistd -n vumi_http_proxy --help

.. warning::

   This version does not yet support HTTPS requests
