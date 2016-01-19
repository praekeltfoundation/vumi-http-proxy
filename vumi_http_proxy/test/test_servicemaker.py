from vumi_http_proxy.servicemaker import Options, ProxyWorkerServiceMaker
from twisted.trial import unittest


class TestOptions(unittest.TestCase):
    def test_defaults(self):
        options = Options()
        options.parseOptions([])
        self.assertEqual(options["port"], 8080)
        self.assertEqual(str(options["interface"]), "0.0.0.0")

    def test_override(self):
        options = Options()
        options.parseOptions(["--port", 8000])
        options.parseOptions(["--interface", "127.0.0.1"])
        self.assertEqual(options["port"], "8000")
        self.assertEqual(str(options["interface"]), "127.0.0.1")


class TestProxyWorkerServiceMaker(unittest.TestCase):
    def test_makeService(self):
        self.assertEqual(
          str(ProxyWorkerServiceMaker.makeService),
          '<unbound method ProxyWorkerServiceMaker.makeService>')
