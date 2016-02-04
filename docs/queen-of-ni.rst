Click queen-of-ni Usage
================================

This plugin allows manual configuration of the HTTP Proxy (but with a cool name).

First, build this locally::

	$ virtualenv ve
	$ source ve/bin/activate
	(ve)$ pip install -e .

In order to run queen-of-ni a blacklist file must be specified. This must be a PyYAML configuration file - an example of which can 
be found in ./docs/proxy_blacklist.yml
The default settings are::

	IP address: 0.0.0.0
	port: 8080
	blacklist: None

To run queen-of-ni using default configuration, run::

	(ve)$ queen-of-ni --blacklist BLACKLISTFILENAME

Otherwise to use manual configuration, run::

	(ve)$ queen-of-ni --interface IPADDRESS --port PORTNO --blacklist BLACKLISTFILENAME

For help, see::

	(ve)$ queen-of-ni --help