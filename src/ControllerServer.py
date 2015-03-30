#!/bin/python

# Services exposed by the VM Manager
# The REST url : 
# http://host-name/api/1.0/disk-usage
# http://host-name/api/1.0/running-time 
# http://host-name/api/1.0/mem-usage
# http://host-name/api/1.0/running-processes
# http://host-name/api/1.0/cpu-load
# http://host-name/api/1.0/execute/<command>

import urlparse
import os
import os.path
import json

# bunch of tornado imports
import tornado.httpserver 
import tornado.ioloop 
import tornado.options 
import tornado.web
from tornado.options import define, options
from http_logging.http_logger import logger
from utils.envsetup import EnvSetUp
import Controller



define("port", default=8000, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

    def post(self):
        post_data = dict(urlparse.parse_qsl(self.request.body))
        c = Controller.Controller()
        self.write(c.test_lab(post_data['lab_id'], post_data['lab_src_url'], post_data.get('version', None)))


if __name__ == "__main__":
    e = EnvSetUp()
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", MainHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug = True)

    http_server = tornado.httpserver.HTTPServer(app)
    config_spec = json.loads(open(e.get_ovpl_directory_path() + "/config/config.json").read())
    options.port = config_spec["CONTROLLER_CONFIG"]["SERVER_PORT"]
    logger.debug("ControllerServer: It will run on port : " + str(options.port))
    http_server.listen(options.port) 
    tornado.ioloop.IOLoop.instance().start()
