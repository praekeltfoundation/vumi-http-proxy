from twisted.web import server, resource
from twisted.internet import reactor, defer
from twisted.internet.defer import inlineCallbacks, returnValue, succeed
from twisted.internet.endpoints import serverFromString
from twisted.test import proto_helpers
from vumi_http_proxy.http_proxy import ProxyFactory


DEFAULT_TIMEOUT = 2
hostnames = {'zombo.com': '69.16.230.117',
             'zombie.com': '66.96.162.142',
             '127.0.0.1': '127.0.0.1'}


class HttpTestResource(resource.Resource):

    isLeaf = True

    def render_GET(self, request):
        return "<html>Allowed</html>"


class HttpTestServer(object):

    def __init__(self, testcase):
        self.site = server.Site(HttpTestResource())
        self.server = None
        testcase.addCleanup(self.cleanup)

    @inlineCallbacks
    def start(self):
        server_endpoint = serverFromString(
            reactor, "tcp:0:interface=127.0.0.1")
        self.server = yield server_endpoint.listen(self.site)
        returnValue(self.server.getHost().port)

    @inlineCallbacks
    def cleanup(self):
        if self.server is not None:
            yield self.server.stopListening()


class TestResolver(object):
    def __init__(self):
        self.hostnames = hostnames

    def getHostByName(self, name, timeout=None, effort=10):
        d = defer.Deferred()
        ip = self.hostnames.get(name)
        reactor.callLater(0.5, d.callback, ip)
        return d


class TestAgent(object):
    def request(self, method, uri, headers, bodyProducer):
        # ?
        return succeed


class TestInitialize(object):
    @inlineCallbacks
    def main(self):
        resolver = TestResolver
        http_client = TestAgent
        proxy = ProxyFactory(['69.16.230.117'], resolver, http_client)
        server_endpoint = serverFromString(
            reactor, "tcp:%d:interface=%s" % (self.port, self.ip))
        server = yield server_endpoint.listen(proxy)
        self.addCleanup(server.stopListening)
        returnValue(server.getHost().port)

    def getServer(self):
        return server


class TestInitializeSTR(object):
    def main(self):
        resolver = TestResolver
        http_client = TestAgent
        factory = ProxyFactory('69.16.230.117', resolver, http_client)
        self.proto = factory.buildProtocol(('0.0.0.0', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)
        return self.tr, self.proto
