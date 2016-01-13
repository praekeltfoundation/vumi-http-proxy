from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.endpoints import serverFromString, clientFromString
from twisted.trial import unittest
from twisted.test import proto_helpers
from twisted.web.client import ProxyAgent, readBody

from vumi_http_proxy.http_proxy import ProxyFactory


class CheckProxyRequestTestCase(unittest.TestCase):
    def setUp(self):
        factory = ProxyFactory()
        self.proto = factory.buildProtocol(('0.0.0.0', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def test_artisanal(self):
        self.proto.dataReceived("\r\n".join([
            "GET http://zombo.com/ HTTP/1.1",
            "Host: zombo.com",
            "",
            "",
        ]))
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

    @inlineCallbacks
    def test_with_client(self):
        server_endpnt = serverFromString(reactor, "tcp:0:interface=127.0.0.1")
        server = yield server_endpnt.listen(ProxyFactory())
        self.addCleanup(server.stopListening)
        port = server.getHost().port

        client_endpoint = clientFromString(
            reactor, "tcp:host=localhost:port=%s" % (port,))
        agent = ProxyAgent(client_endpoint)
        response = yield agent.request("GET", "http://zombo.com/")
        response_body = yield readBody(response)

        self.assertEqual(response.code, 400)  # TODO: This should be 400.
        self.assertEqual(response_body, "<html>Denied</html>")
