"""my very basic proxy using twisted.web.proxy.Proxy(HTTPChannel)"""

from twisted.web import http, proxy
from twisted.web.proxy import ProxyRequest
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory

"""What does this do?
f = http.HTTPFactory()
f.protocol = ProxyFactory"""


# Set up proxy


class ProxyFactory(http.HTTPFactory):
    def buildProtocol(self, addr):
        return proxy.Proxy()


# My attempt to subclass proxyRequest


class CheckProxyRequest(ProxyRequest):
    def process(self):
        self.checkHeaders()
        return ProxyRequest.process(self)
    def checkHeaders(self):
        # how to read header and path?
        self.requestHeaders



"""class ResourceFactory(Resource):
site = ProxyRequest.path
print site"""

# Setting up server


class QOTD(Protocol):
    def connectionMade(self):
        self.transport.write(ProxyRequest.path)
        self.transport.loseConnection()


class QOTDFactory(Factory):
    def buildProtocol(self, addr):
        return QOTD()

# Connect

reactor.listenTCP(8080, ProxyFactory())
reactor.run()

# TODO include timeOut = no of seconds and then resetTimeout
# TODO include blacklist of ips
# TODO get the right port
