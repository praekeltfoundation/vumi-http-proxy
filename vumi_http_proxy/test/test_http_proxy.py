from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, Deferred, returnValue
from twisted.internet.endpoints import serverFromString, clientFromString
from twisted.trial import unittest
from twisted.test import proto_helpers
from twisted.web.client import ProxyAgent, readBody

from vumi_http_proxy.http_proxy import ProxyFactory

from .helpers import HttpTestServer, DEFAULT_TIMEOUT


class TestProxyToLocalServer(unittest.TestCase):

    timeout = DEFAULT_TIMEOUT

    def setUp(self):
        self.server = HttpTestServer(self)

    @inlineCallbacks
    def setup_proxy(self, blacklist):
        proxy = ProxyFactory(blacklist)
        server_endpoint = serverFromString(
            reactor, "tcp:0:interface=127.0.0.1")
        server = yield server_endpoint.listen(proxy)
        self.addCleanup(server.stopListening)
        returnValue(server.getHost().port)

    @inlineCallbacks
    def make_request(self, proxy_port, url):
        client_endpoint = clientFromString(
            reactor, "tcp:host=localhost:port=%s" % (proxy_port,))
        agent = ProxyAgent(client_endpoint)
        response = yield agent.request("GET", url)
        body = yield readBody(response)
        returnValue((response, body))

    @inlineCallbacks
    def check_proxy_request(self, blacklist, expected_code, expected_body):
        http_port = yield self.server.start()
        proxy_port = yield self.setup_proxy(blacklist)
        url = 'http://127.0.0.1:%s/' % (http_port,)
        response, body = yield self.make_request(proxy_port, url)
        self.assertEqual(response.code, expected_code)
        self.assertEqual(body, expected_body)

    def test_allow(self):
        return self.check_proxy_request([], 200, '<html>Allowed</html>')

    def test_deny(self):
        return self.check_proxy_request(
            ["127.0.0.1"], 400, "<html>Denied</html>")


class TestCheckProxyRequest(unittest.TestCase):

    timeout = DEFAULT_TIMEOUT

    def setUp(self):
        factory = ProxyFactory(['69.16.230.117'])
        self.proto = factory.buildProtocol(('0.0.0.0', 0))
        self.tr = proto_helpers.StringTransportWithDisconnection()
        self.proto.makeConnection(self.tr)

    @inlineCallbacks
    def test_artisanal_deny(self):
        d = Deferred()

        def lost(*args, **kw):
            print "LOST", args, kw
            d.callback(None)

        self.tr.loseConnection = lost
        self.proto.connectionLost = lost
 
        self.proto.dataReceived("\r\n".join([
            "GET http://zombo.com/ HTTP/1.1",
            "Host: zombo.com",
            "",
            "",
        ]))
        
        print "WAIT"
        print self.tr.value()
        yield d
        print "YAY"

        self.assertEqual(self.tr.value(), "\r\n".join([
            "HTTP/1.1 400 Bad Request",
            "Transfer-Encoding: chunked",
            "",
            "13",
            "<html>Denied</html>",
            "0",
            "",
            "",
        ]))

    def _test_artisanal_allow(self):
        self.proto.dataReceived("\r\n".join([
            "GET http://zombie.com/ HTTP/1.1",
            "Host: zombie.com",
            "",
            "",
        ]))
        d = Deferred()
        reactor.callLater(1, d.callback, None)
        yield d
        self.assertTrue(self.tr.value().startswith("HTTP/1.1 200 OK"))
