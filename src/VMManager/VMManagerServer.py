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
import __init__

# bunch of tornado imports
import tornado.httpserver 
import tornado.ioloop 
import tornado.options 
import tornado.web
from tornado.options import define, options
from http_logging.http_logger import logger
from utils.envsetup import EnvSetUp

import VMManager

define("port", default=9089, help="run on the given port", type=int)


class DiskUsageHandler(tornado.web.RequestHandler):
    def get(self):
        #response = VMManager.disk_usage()
        self.write(VMManager.disk_usage())


class CPULoadHandler(tornado.web.RequestHandler):
    def get(self):    
        self.write(VMManager.cpu_load())


class RunningTimeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(VMManager.running_time())


class RunningProcHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(VMManager.running_processes())


class MemUsageHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(VMManager.mem_usage())  


class ExecuteHandler(tornado.web.RequestHandler):
    def get(self, command):
        self.write(VMManager.execute(command))


class TestLabHandler(tornado.web.RequestHandler):
    def post(self):
        post_data = dict(urlparse.parse_qsl(self.request.body))
        logger.info("VMManagerServer: TestLabHandler: post(): post_data = %s" % str(post_data))
        self.write(VMManager.test_lab(post_data['lab_src_url'], post_data.get('version', None)))

    def get(self):
        logger.info("VMManagerServer: TestLabHandler: get()")
        self.write("Hello World")


if __name__ == "__main__":

    e = EnvSetUp()
    logger.info("VMManagerServer: __main()")
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/api/1.0/disk-usage", DiskUsageHandler),
            (r"/api/1.0/mem-usage", MemUsageHandler),
            (r"/api/1.0/running-time", RunningTimeHandler),
            (r"/api/1.0/running-processes", RunningProcHandler),
            (r"/api/1.0/cpu-load", CPULoadHandler),
            (r"/api/1.0/execute/([\w*\d*\%\-]+)", ExecuteHandler),
            (r"/api/1.0/test-lab", TestLabHandler)
        ],
        debug = False)
    http_server = tornado.httpserver.HTTPServer(app) 
    http_server.listen(options.port) 
    tornado.ioloop.IOLoop.instance().start()
