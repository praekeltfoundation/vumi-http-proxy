from twisted.python import log
from twisted.web import http, proxy
from twisted.internet import reactor
from twisted.internet.endpoints import serverFromString
from twisted.names import client

# blacklist of disallowed domains (change this to ips later, and move)

BLACKLIST_HOSTS = ["facebook.com", "twitter.com", "zombo.com"]
DEFAULT_BLACKLIST = ["69.16.230.117"]

#  Set up proxy


class ProxyFactory(http.HTTPFactory):

    def __init__(self, blacklist):
        http.HTTPFactory.__init__(self)
        self.blacklist = blacklist

    def buildProtocol(self, addr):
        return Proxy(self.blacklist)


# Check request
class CheckProxyRequest(proxy.ProxyRequest):
    def process(self):
        host, _, port = self.getAllHeaders()['host'].partition(':')
        d = client.getHostByName(str(host))
        d.addCallback(self.setIP, str(host))
        d.addErrback(self.handleError)

    def handleError(self, failure):
        log.err(failure)
        self.setResponseCode(400)
        self.write("<html>Denied</html>")
        self.finish()
        return

    def setIP(self, ip_addr, host):
        print ip_addr
        print "!!"+self.channel.blacklist[0]
        if ip_addr in DEFAULT_BLACKLIST:
            print "IN"
            self.setResponseCode(400)
            self.write("<html>Denied</html>")
            self.finish()
            return
        elif ip_addr is None:
            print "ERR"
            self.write("<html>ERROR: No IP adresses found for name %r" %
                       host + " </html>")
            self.finish()
            return
        return proxy.ProxyRequest.process(self)


class Proxy(proxy.Proxy):

    requestFactory = CheckProxyRequest

    def __init__(self, blacklist):
        proxy.Proxy.__init__(self)
        self.blacklist = blacklist


class Initialize(object):
    def __init__(self, blacklist, ip, port):
        if not blacklist:
            blacklist = DEFAULT_BLACKLIST
        self.blacklist = blacklist
        self.ip = ip
        self.port = port

    def main(self):
        factory = ProxyFactory(self.blacklist)
        endpoint = serverFromString(
            reactor, "tcp:%d:interface=%s" % (self.port, self.ip))
        endpoint.listen(factory)
        reactor.run()
