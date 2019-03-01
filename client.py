# -*- coding: utf-8 -*-

import thriftpy
from thriftpy.rpc import client_context,make_client

import json
from config import *
from utils import build_class
from utils import build_json

microservice_thrift = thriftpy.load(thrift_file, module_name)
REQ_CLASS = getattr(microservice_thrift, req_class_name)
RESP_CLASS = getattr(microservice_thrift, resp_class_name)

with open(req_data_file) as fd:
    req_data = json.loads(fd.read())

class ThriftClient():
    def __init__(self, host, port, service_name):
        self.service = getattr(microservice_thrift, service_name)
        self.client = make_client(self.service, host, port)

    def request(self, api_name, req):
        resp = self.client._req(api_name, req=req)
        print resp

if __name__=='__main__':
    client = ThriftClient(host, port, service_name)

    #print REQ_CLASS.__dict__

    req = build_class(REQ_CLASS, req_data)
    client.request(api_name, req=req)

