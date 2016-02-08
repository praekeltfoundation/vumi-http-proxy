"""Proxy generator to resolve and check client HTTP requests

.. moduleauthor:: Carla Wilby <thisiscarlawilby@gmail.com>

"""

from twisted.python import log
from twisted.web import http, proxy
from twisted.internet import reactor
from twisted.internet.endpoints import serverFromString
from twisted.names import client
from twisted.web.client import Agent, readBody
from urlparse import urlparse, urlunparse
from twisted.internet.defer import inlineCallbacks, succeed


class ProxyFactory(http.HTTPFactory):

    def __init__(self, blacklist, resolver, http_client):
        http.HTTPFactory.__init__(self)
        self.blacklist = blacklist
        self.resolver = resolver
        self.http_client = http_client

    def buildProtocol(self, addr):
        return Proxy(self.blacklist, self.resolver, self.http_client)


class CheckProxyRequest(proxy.ProxyRequest):
    """
    Receives request, processes request and returns response
    """
    def process(self):
        """ Attain hostname, return deferred on resolver.getHostByName
        """
        host, _, port = self.getAllHeaders()['host'].partition(':')
        d = self.channel.resolver.getHostByName(host)
        d.addCallback(self.setIP, host)
        d.addErrback(self.handleError)
        return d

    def handleError(self, failure):
        log.err(failure)
        self.setResponseCode(400)
        self.write("<html>Denied</html>")
        self.finish()
        return

    def setIP(self, ip_addr, host):
        """
        Process corresponding ip address to allow or deny.
        """
        if not ip_addr:
            self.setResponseCode(400)
            self.write("<html>ERROR: No IP adresses found for name %r" %
                       host + " </html>")
            self.finish()
            return
        if ip_addr in self.channel.blacklist:
            self.setResponseCode(400)
            self.write("<html>Denied</html>")
            self.finish()
            return
        uri = self.replaceHostWithIP(self.uri, ip_addr)
        headers = self.requestHeaders
        d = self.channel.http_client.request(
            self.method, uri, headers, StringProducer(self.content.read()))
        d.addCallback(self.sendResponseBack)
        return d

    def replaceHostWithIP(self, uri, ip_addr):
        """
        Parse request to find host, replace with IP and port (if applicable).
        """
        scheme, netloc, path, params, query, fragment = urlparse(uri)
        _, _, port = netloc.partition(':')
        if port:
            ip_addr = "%s:%s" % (ip_addr, port)
        return urlunparse((scheme, ip_addr, path, params, query, fragment))

    @inlineCallbacks
    def sendResponseBack(self, r):
        """
        Fetch response and response code, send to client.
        """
        self.setResponseCode(r.code)
        for key, value in r.headers.getAllRawHeaders():
            self.responseHeaders.addRawHeader(key, value)
        body = yield readBody(r)
        self.write(body)
        self.finish()


class StringProducer(object):
    """
    Parse response body.
    """
    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


class Proxy(proxy.Proxy):
    """
    Start proxy with CheckProxyRequest as requestFactory.
    """
    requestFactory = CheckProxyRequest

    def __init__(self, blacklist, resolver, http_client):
        proxy.Proxy.__init__(self)
        self.blacklist = blacklist
        self.resolver = resolver
        self.http_client = http_client


class Initialize(object):
    """
    This class initialises the proxy based on the configuration specified
    """
    def __init__(self, blacklist, dnsservers, ip, port):
        self.blacklist = blacklist
        self.dnsservers = dnsservers
        self.ip = ip
        self.port = port

    def main(self):
        """
        :param blacklist: List of disallowed ip addresses.
        :type blacklist: list
        :param dnservers: List of manual dns servers to use.
        :type dnsservers: list
        :param ip: Address of server to initialize proxy
        :type ip: str
        :param port: Port of server to initialize proxy
        :type port: int
        """
        resolver = client.createResolver(self.dnsservers)
        http_client = Agent(reactor)
        factory = ProxyFactory(self.blacklist, resolver, http_client)
        endpoint = serverFromString(
            reactor, "tcp:%d:interface=%s" % (self.port, self.ip))
        endpoint.listen(factory)
        reactor.run()
