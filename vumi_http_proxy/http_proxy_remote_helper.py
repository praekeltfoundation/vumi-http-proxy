# -*- test-case-name: vumi_http_proxy.test.test_http_proxy -*-

from twisted.protocols import basic
from twisted.internet import protocol
from vumi_http_proxy.http_proxy import CheckProxyRequest


class HttpProxy(object):
    def __init__(self):
        self.checkRequest = CheckProxyRequest()


class RemoteProtocol(basic.LineReceiver):
    def __init__(self):
        self.proxy = HttpProxy()

    def lineReceived(self, line):
        # This is where 'zombo.com' and processed and passed to test_http_proxy
        path = self.checkRequest.process(line)
        self.sendLine(path)


class RemoteFactory(protocol.Factory):
    protocol = RemoteProtocol

    def main():
        from twisted.internet import reactor
        from twisted.python import log
        import sys
        log.startLogging(sys.stdout)
        reactor.listenTCP(0, RemoteFactory())
        reactor.run()

if __name__ == "__main__":
    main()
