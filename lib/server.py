#coding=utf-8
import logging
logging.basicConfig()

import sys

import thriftpy2 as thriftpy
from thriftpy.rpc import make_server

from config import *
from utils import *

import types

class MakeMockData(object):
    def __init__(self, microservice_thrift, module_name, service):
        self.microservice_thrift = microservice_thrift
        self.service = service
        self.resp_data = {}

    def gen_response(self, api_name):
        RESP_CLASS = getattr(self.service, api_name + '_result')

        resp = build_class(RESP_CLASS, self.resp_data.get(api_name, None))
        print resp
        return resp

    def init_generator(self):
        for api_name in self.service.__dict__["thrift_services"]:
            my_func = init_func_generator(self.__class__.__name__, api_name, [('req', None)])
            setattr(self, api_name, types.MethodType(my_func, self))

    def update_mock_resp(self, api_name, api_data):
        self.resp_data[api_name] = api_data

class ThriftServer():
    def __init__(self, conf_file):
        parser = ConfigParser(conf_file)
        conf = parser.conf["server"]

        self.microservice_thrift = thriftpy.load(conf["thrift_file"], conf["module_name"])
        self.service = getattr(self.microservice_thrift, conf["service_name"])

        self.handler = MakeMockData(self.microservice_thrift, conf["module_name"], self.service)
        self.handler.init_generator()

        self.server = make_server(self.service, self.handler, conf["host"], int(conf["port"]))

    def startServer(self):
        print "mock server start "
        self.server.serve()
        print "OK "

    def close(self):
        self.server.close()

    def update_mock_resp(self, api_name, mock_data):
         self.handler.update_mock_resp(api_name, mock_data)

if __name__=='__main__':
    server = ThriftServer(sys.argv[1]) 
    server.startServer()

