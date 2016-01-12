from vumi_http_proxy.http_proxy import CheckProxyRequest
from twisted.trial import unittest
from twisted.test import proto_helpers


class CheckProxyRequestTestCase(unittest.TestCase):
    def setUp(self):
        factory = ProxyFactory()
        self.proto = factory.buildProtocol(('0.0.0.0', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def _test(self, operation a, b, expected):
        self.proto.dataReceived('%s %d %d\r\n' % (operation))
        self.assertEqual(int(self.tr.value()), expected)

    def test_failure(self):
        conn = factory.buildProtocol('127.0.0.1', 0)
        # how is this supposed to fail?
        return self.assertFailure(d, ConnectionRefusedError)

    def test_process(self):
        checkRequest = CheckProxyRequest()
        result = CheckProxyRequest.process()
        self.assertEqual(result, "something")
