"""my very basic proxy using twisted.web.proxy.Proxy(HTTPChannel)"""

from twisted.web import http, proxy
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.web import server, resource

# blacklist of disallowed domains (can change this to ips later)

blacklist = ["facebook.com", "twitter.com", "zombo.com"]

# 1. Set up proxy


class ProxyFactory(http.HTTPFactory):
    def buildProtocol(self, addr):
        return proxy.Proxy()


class Proxy(proxy.Proxy):
    requestFactory = proxy.ProxyRequest


class ProxyRequest(proxy.ProxyRequest):
    protocols = dict(http=proxy.ProxyClientFactory)


class ProxyClientFactory(proxy.ProxyClientFactory):
    protocol = proxy.ProxyClient


# 2. Check request

class CheckProxyRequest(proxy.ProxyRequest):
    def process(self):
        if self.path in blacklist:
            site


# 3. Return page for blocked site (if applicable)

class notAllowed(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        return "<html>Sorry, you are not allowed access here.</html>"


"""class URL(Resource):
    isLeaf = True

    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    def render_GET(self, request):
        if self.
    return request.prepath"""


"""class ResourceFactory(Resource):
site = ProxyRequest.path
print site"""

# Connect
site = server.Site(notAllowed())
reactor.listenTCP(8080, ProxyFactory())
reactor.run()

# TODO include timeOut = no of seconds and then resetTimeout
# TODO include blacklist of ips
# TODO get the right port
# TODO Make deferreds
