#!/usr/bin/env python

from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.internet.endpoints import serverFromString
from twisted.internet import reactor
from vumi_http_proxy.http_proxy import ProxyFactory


class Options(usage.Options):
    optParameters = [["port", None, 8080,
                     "The port number to start the proxy"],
                     ["interface", None, "0.0.0.0", "IP to start proxy on"]]


class ProxyWorkerServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "proxy_worker"
    description = "Service maker to launch proxy from given port and ip addr"
    options = Options

    def makeService(self, options):
        """ Call Initialize to start endpoint server """
        factory = ProxyFactory(["asdf.com"])
        endpoint = serverFromString(
            reactor, "tcp:%d:interface=%s" % (
                options["port"], str(options["interface"])))
        # import pdb; pdb.set_trace()
        endpoint.listen(factory)
        # What oh what do I return?
        return endpoint
        # ERR: AttributeError: 'TCP4ServerEndpoint' object has no
        # attribute 'setServiceParent'
        # egs of what has been returned in other examples:
        # return internet.TCPServer(int(options["port"]), MyFactory())
        # no return, but: service.setServiceParent(application)
        # another one has: service = StreamServerEndpointService(endpoint,
        # factory)
        # ... service.setServiceParent(application)
        # But ^ is in a .tac file.

serviceMaker = ProxyWorkerServiceMaker()
