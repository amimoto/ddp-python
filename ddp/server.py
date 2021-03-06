import tornado.httpserver
import tornado.ioloop
import tornado.web
from sockjs.tornado import transports, SockJSRouter
import socket

class Server(object):
    def __init__(self, handler, baseurl, port):
        self.port = port
        self.baseurl = baseurl
        router = SockJSRouter(handler, self.baseurl)
        # Meteor doesn't obey sockjs url conventions so we patch it on our end to work around
        newurls = []
        for url in router._transport_urls:
            if "websocket" in url[0]:
                newurls.append(url)
            newurls.append((url[0].replace(self.baseurl, self.baseurl + '/sockjs'), url[1], url[2]))
        router._transport_urls = newurls
        self.application = tornado.web.Application(router.urls)

    def start(self):
        self.http_server = tornado.httpserver.HTTPServer(self.application)
        self.http_server.listen(self.port)
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.ioloop.start()


if __name__ == "__main__":
    import handler
    server = Server(handler.Handler)
    server.start()

