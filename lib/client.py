# -*- coding: utf-8 -*-
import thriftpy2 as thriftpy
from thriftpy2.rpc import client_context,make_client

import json
from config import ConfigParser
from utils import build_class
from utils import build_json

class ThriftClient():
    def __init__(self, conf_file):
        parser = ConfigParser(conf_file)
        conf = parser.conf["server"]

        self.microservice_thrift = thriftpy.load(conf["thrift_file"], conf["module_name"])
        self.service = getattr(self.microservice_thrift, conf["service_name"])
        self.client = make_client(self.service, conf["host"], int(conf["port"]))

    def request(self, api_name, req_class_name, resp_class_name, req_data):
        REQ_CLASS = getattr(self.microservice_thrift, req_class_name)
        RESP_CLASS = getattr(self.microservice_thrift, resp_class_name)

        req = build_class(REQ_CLASS, req_data)
        resp = self.client._req(api_name, req=req)
        return build_json(resp)

    def close(self):
        self.client.close()

if __name__=='__main__':
    api_name = 'GenFilter'
    req_class_name = 'GenFiltersRequest'
    resp_class_name = 'GenFiltersResponse'
    req_data_file = './data/req.json'

    with open(req_data_file) as fd:
        req_data = json.loads(fd.read())

    client = ThriftClient("conf/server.conf")
    resp = client.request(api_name, req_class_name, resp_class_name, req_data)
    print resp
