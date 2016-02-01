#!/usr/bin/env python

from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import strports
from vumi_http_proxy.http_proxy import ProxyFactory
from twisted.names import client
from twisted.web.client import Agent
from twisted.internet import reactor


class Options(usage.Options):
    optParameters = [["port", None, 8080,
                     "The port number to start the proxy"],
                     ["interface", None, "0.0.0.0", "IP to start proxy on"]]
    optFlags = [["--port", "-p", "The port number to start the proxy"],
                ["--interface", "-i", "IP to start proxy on"]]


class ProxyWorkerServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "vumi_http_proxy"
    description = "Service maker to launch proxy from given port and ip addr"
    options = Options

    def makeService(self, options):
        factory = ProxyFactory(
            ["zombo.com"], client.createResolver(), Agent(reactor))
        return strports.service("tcp:%d:interface=%s" % (
                options["port"], str(options["interface"])), factory)
