from vumi_http_proxy.http_proxy import CheckProxyRequest
from twisted.trial import unittest
from twisted.test import proto_helpers


class ProxyFactoryTestCase(unittest.TestCase):
    def setUp(self):
        factory = ProxyFactory()
        self.proto = factory.buildProtocol(('0.0.0.0', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def test_buildProtocol(self, addr):
        cfactory = ProxyFactory()
        result = ProxyFactory.buildProtocol()
        self.assertEqual(result, "something")


class CheckProxyRequestTestCase(unittest.TestCase):
    def test_process(self):
        checkRequest = CheckProxyRequest()
        result = CheckProxyRequest.process()
        self.assertEqual(result, "something")
