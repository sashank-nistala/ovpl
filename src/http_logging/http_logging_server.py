#!/usr/bin/env python
# Authors : Nitish,Siddharth
# Organization : VLEAD, Virtual-Labs
# Services exposed by LoggingServer
# http://host-name/log/

import threading
import time
import json
import os


# tornado imports
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import define, options

import __init__
from utils.envsetup import EnvSetUp
import helper

define("port", default=8239, help="run on the given port", type=int)

class LogHandler(tornado.web.RequestHandler):
    def get(self):
        print "Hello World"

    def post(self):
        """Spawns a new thread for every request and passes the request as \
        arguments to log() function"""
        t = threading.Thread(target=helper.log,
                             args=(self.request.arguments,))
        t.start()


class OtherHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        pass

if __name__ == "__main__":
    e = EnvSetUp()    
    app = tornado.web.Application(
        handlers=[
            (r"/log/.*", LogHandler),
            (r"/.*", OtherHandler),
        ],
        debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    config_spec = json.loads(open(e.get_ovpl_directory_path() + "/config/config.json").read())
    options.port = config_spec["LOGGING_CONFIGURATION"]["LOGSERVER_CONFIGURATION"]["SERVER_PORT"]
    http_server.bind(options.port)
    http_server.start(1)
    print "http logging service started"
    tornado.ioloop.IOLoop.instance().start()

