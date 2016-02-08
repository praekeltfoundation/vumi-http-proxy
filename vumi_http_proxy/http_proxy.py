from twisted.python import log
from twisted.web import http, proxy
from twisted.internet import reactor
from twisted.internet.endpoints import serverFromString
from twisted.names import client
from twisted.web.client import Agent, readBody
from urlparse import urlparse, urlunparse
from twisted.internet.defer import inlineCallbacks, succeed
from twisted.internet.protocol import Protocol, ClientFactory


class ProxyFactory(http.HTTPFactory):

    def __init__(self, blacklist, resolver, http_client):
        http.HTTPFactory.__init__(self)
        self.blacklist = blacklist
        self.resolver = resolver
        self.http_client = http_client

    def buildProtocol(self, addr):
        return Proxy(self.blacklist, self.resolver, self.http_client)


class CheckProxyRequest(proxy.ProxyRequest):
    def process(self):
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
        if self.method == 'CONNECT':
            self.processConnectRequest()
        else:
            uri = self.replaceHostWithIP(self.uri, ip_addr)
            headers = self.requestHeaders
            d = self.channel.http_client.request(
                self.method, uri, headers, StringProducer(self.content.read()))
            d.addCallback(self.sendResponseBack)
            return d

    def replaceHostWithIP(self, uri, ip_addr):
        scheme, netloc, path, params, query, fragment = urlparse(uri)
        _, _, port = netloc.partition(':')
        if port:
            ip_addr = "%s:%s" % (ip_addr, port)
        return urlunparse((scheme, ip_addr, path, params, query, fragment))

    @inlineCallbacks
    def sendResponseBack(self, r):
        self.setResponseCode(r.code)
        for key, value in r.headers.getAllRawHeaders():
            self.responseHeaders.addRawHeader(key, value)
        body = yield readBody(r)
        self.write(body)
        self.finish()

    def splitHostPort(self, hostport, default_port):
        port = default_port
        parts = hostport.split(':', 1)
        try:
            port = int(parts[1])
        except ValueError:
            self.write("Bad CONNECT Request",
                       "Unable to parse port from URI: %s" % repr(self.uri))
            self.finish()
        return parts[0], port

    def processConnectRequest(self):
        parsed = urlparse(self.uri)
        default_port = self.ports.get(parsed.scheme)
        host, port = self.splitHostPort(parsed.netloc or parsed.path,
                                        default_port)
        clientFactory = ConnectProxyClientFactory(host, port, self)
        self.reactor.connectTCP(host, port, clientFactory)


class ConnectProxy(proxy.Proxy):
    """HTTP Server Protocol that supports CONNECT"""
    requestFactory = CheckProxyRequest
    connectedRemote = None

    def requestDone(self, request):
        if request.method == 'CONNECT' and self.connectedRemote is not None:
            self.connectedRemote.connectedClient = self
        else:
            Proxy.requestDone(self, request)

    def connectionLost(self, reason):
        if self.connectedRemote is not None:
            self.connectedRemote.transport.loseConnection()
        Proxy.connectionLost(self, reason)

    def dataReceived(self, data):
        if self.connectedRemote is None:
            Proxy.dataReceived(self, data)
        else:
            # Once proxy is connected, forward all bytes received
            # from the original client to the remote server.
            self.connectedRemote.transport.write(data)


class ConnectProxyClient(Protocol):
    connectedClient = None

    def connectionMade(self):
        self.factory.request.channel.connectedRemote = self
        self.factory.request.setResponseCode(200, "CONNECT OK")
        self.factory.request.setHeader('X-Connected-IP',
                                       self.transport.realAddress[0])
        self.factory.request.setHeader('Content-Length', '0')
        self.factory.request.finish()

    def connectionLost(self, reason):
        if self.connectedClient is not None:
            self.connectedClient.transport.loseConnection()

    def dataReceived(self, data):
        if self.connectedClient is not None:
            # Forward all bytes from the remote server back to the
            # original connected client
            self.connectedClient.transport.write(data)
        else:
            log.msg("UNEXPECTED DATA RECEIVED:", data)


class ConnectProxyClientFactory(ClientFactory):
    protocol = ConnectProxyClient

    def __init__(self, host, port, request):
        self.request = request
        self.host = host
        self.port = port

    def clientConnectionFailed(self, connector, reason):
        self.request.fail("Gateway Error", str(reason))


class StringProducer(object):
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

    requestFactory = CheckProxyRequest

    def __init__(self, blacklist, resolver, http_client):
        proxy.Proxy.__init__(self)
        self.blacklist = blacklist
        self.resolver = resolver
        self.http_client = http_client


class Initialize(object):
    def __init__(self, blacklist, dnsservers, ip, port):
        self.blacklist = blacklist
        self.dnsservers = dnsservers
        self.ip = ip
        self.port = port

    def main(self):
        resolver = client.createResolver(self.dnsservers)
        http_client = Agent(reactor)
        factory = ProxyFactory(self.blacklist, resolver, http_client)
        endpoint = serverFromString(
            reactor, "tcp:%d:interface=%s" % (self.port, self.ip))
        endpoint.listen(factory)
        reactor.run()
