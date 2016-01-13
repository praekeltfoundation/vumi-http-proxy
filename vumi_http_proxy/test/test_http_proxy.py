from twisted.trial import unittest
from twisted.test import proto_helpers

from vumi_http_proxy.http_proxy import ProxyFactory


class CheckProxyRequestTestCase(unittest.TestCase):

    def setUp(self):
        factory = ProxyFactory()
        self.proto = factory.buildProtocol(('0.0.0.0', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def test_process(self):
        self.proto.dataReceived("\r\n".join([
            "GET http://zombo.com/ HTTP/1.1",
            "Host: zombo.com",
            "",
            "",
        ]))

        self.assertEqual(self.tr.value(), "\r\n".join([
            "HTTP/1.1 200 OK",
            "Transfer-Encoding: chunked",
            "",
            "13",
            "<html>Denied</html>",
            "0",
            "",
            "",
        ]))
