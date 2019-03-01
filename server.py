#coding=utf-8

import thriftpy
from thriftpy.rpc import make_server

from config import *
from utils import build_class
from utils import build_json

microservice_thrift = thriftpy.load(thrift_file, module_name=module_name)
REQ_CLASS = getattr(microservice_thrift, req_class_name)
RESP_CLASS = getattr(microservice_thrift, resp_class_name)

class Dispatcher(object):
    def Hi(self, args):
        """
        input: args is REQ_CLASS
        output: resp is RESP_CLASS
        """
        name = args.Name
        resp = RESP_CLASS(Resp="Your Name is " + name)

        print "doReponse! ", args.Name, resp
        return resp

class ThriftServer():
    def __init__(self, host, port, handler, service_name):
        self.service = getattr(microservice_thrift, service_name)
        self.server = make_server(self.service, handler, host, port)

    def startServer(self):
        self.server.serve()

if __name__=='__main__':
    handler = Dispatcher()
    server = ThriftServer(host, port, handler, service_name)

    #print microservice_thrift.__dict__.items()
    #print server.__dict__["server"].__dict__.items()

    server.startServer()

