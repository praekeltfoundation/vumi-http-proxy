from twisted.web import http, proxy
# from twisted.internet import reactor
# from twisted.internet.endpoints import serverFromString

# blacklist of disallowed domains (change this to ips later, and move)

DEFAULT_BLACKLIST = ["facebook.com", "twitter.com", "zombo.com"]

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
        if host in self.channel.blacklist:
            self.setResponseCode(400)
            self.write("<html>Denied</html>")
            self.finish()
            return
        # else allow access to site
        return proxy.ProxyRequest.process(self)


class Proxy(proxy.Proxy):

    requestFactory = CheckProxyRequest

    def __init__(self, blacklist):
        proxy.Proxy.__init__(self)

"""
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
"""
