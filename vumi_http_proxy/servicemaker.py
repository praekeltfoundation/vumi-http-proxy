#!/usr/bin/env python

"""Twistd plugin to launch vumi-http-proxy
    Specify: interface: default 0.0.0.0
             port: default 8080
             configfile: default None

.. moduleauthor:: Carla Wilby <thisiscarlawilby@gmail.com>

"""

from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import strports
from twisted.names import client
from twisted.web.client import Agent, ProxyAgent
from twisted.internet import reactor
from vumi_http_proxy.http_proxy import ProxyFactory
from vumi_http_proxy import config_reader
from twisted.internet.endpoints import TCP4ClientEndpoint


class Options(usage.Options):
    optParameters = [["port", None, "8080",
                     "The port number to start the proxy"],
                     ["interface", None, "0.0.0.0", "IP to start proxy on"],
                     ["configfile", None, None,
                     "Name of the YAML config file for blacklist and servers"]]

    def postOptions(self):
        """
        Check that entered port parses to an integer
        """
        try:
            self["port"] = int(self["port"])
        except (ValueError, TypeError):
            raise usage.UsageError('Port must be an integer. Please try again')


class ProxyWorkerServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "vumi_http_proxy"
    description = "Service maker to launch proxy from given port and ip addr"
    options = Options

    def makeService(self, options):
        """
        Start module with given configuration
        """
        blacklist = config_reader.read_config(options["configfile"])
        endpoint = TCP4ClientEndpoint(
            reactor, options["port"], options["interface"])
        factory = ProxyFactory(
            blacklist, client.createResolver(), Agent(reactor),
            ProxyAgent(endpoint))
        return strports.service("tcp:%d:interface=%s" % (
                options["port"], options["interface"]), factory)
