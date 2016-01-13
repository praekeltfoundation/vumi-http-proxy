from vumi_http_proxy.http_proxy_remote_helper import RemoteFactory
from twisted.trial import unittest
from twisted.test import proto_helpers


class CheckProxyRequestTestCase(unittest.TestCase):
    def setUp(self):
        factory = RemoteFactory()
        self.proto = factory.buildProtocol(('0.0.0.0', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def _test(self, expected):
        self.assertEqual(self.tr.value(), expected)

    def _test_failure(self):
        conn = factory.buildProtocol('127.0.0.1', 0)
        return self.assertFailure(d, ConnectionRefusedError)

    def test_process(self):
        return self._test('zombo.com')

    def test_errorProcess(self):
        return self._test_failure()
