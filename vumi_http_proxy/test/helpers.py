from twisted.web import server, resource
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet.endpoints import serverFromString


DEFAULT_TIMEOUT = 2


class HttpTestResource(resource.Resource):

    isLeaf = True

    def render_GET(self, request):
        return "<html>Allowed</html>"


class HttpTestServer(object):

    def __init__(self, testcase):
        self.site = server.Site(HttpTestResource())
        self.server = None
        testcase.addCleanup(self.cleanup)

    @inlineCallbacks
    def start(self):
        server_endpoint = serverFromString(
            reactor, "tcp:0:interface=127.0.0.1")
        self.server = yield server_endpoint.listen(self.site)
        returnValue(self.server.getHost().port)

    @inlineCallbacks
    def cleanup(self):
        if self.server is not None:
            yield self.server.stopListening()
