#! /usr/bin/env python3

import tornado.ioloop
import tornado.web
from tornado import template

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        t = template.Template("<html>{{ myvalue }}</html>")
        self.write(t.generate(myvalue="XXX"))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()