# -*- test-case-name: vumi_http_proxy.test.test_http_proxy -*-

from twisted.web import http, proxy
from twisted.internet import reactor, defer
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import serverFromString
from twisted.web import server
from twisted.web.resource import Resource

# blacklist of disallowed domains (change this to ips later, and move)

blacklist = ["facebook.com", "twitter.com", "zombo.com"]

#  Set up proxy


class ProxyFactory(http.HTTPFactory):
    def buildProtocol(self, addr):
        return Proxy()


class ProxyRequest(proxy.ProxyRequest):
    protocols = dict(http=proxy.ProxyClientFactory)


class ProxyClientFactory(proxy.ProxyClientFactory):
    protocol = proxy.ProxyClient


# Check request


class CheckProxyRequest(proxy.ProxyRequest):
    def process(self):
        if self.getAllHeaders()['host'] in blacklist:
            # print "Blocked"
            self.write("<html>Denied</html>")
            self.finish()
            return
        # else allow access to site
        return proxy.ProxyRequest.process(self)


class Proxy(proxy.Proxy):
    requestFactory = CheckProxyRequest


# Connect

endpoint = serverFromString(reactor, "tcp:8080:interface=0.0.0.0")
# ERR couldn't listen on 0.0.0.0:80 permission denied
endpoint.listen(ProxyFactory())
reactor.run()

# TODO include timeOut = no of seconds and then resetTimeout
# TODO include blacklist of ips in new file
# TODO Make deferreds
# TODO make ok for http and https
