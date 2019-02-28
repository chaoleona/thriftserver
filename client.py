# -*- coding: utf-8 -*-

import thriftpy

from thriftpy.rpc import client_context,make_client
from zook import ZookWatcher

thrift_file = "hi.thrift"
module_name = "hi_thrift"

microservice_thrift = thriftpy.load(thrift_file, module_name)

class RpcClient():
    def __init__(self, zookhost, appname):
        self.zookhost=zookhost
        self.appname=appname
        self.zookclient=ZookWatcher(hosts=self.zookhost,appname=self.appname)

    def request(self):
        host,port=self.zookclient.getBalanceNode()
        with client_context(microservice_thrift.MicroService, host, port) as c:
            response = c.doResponse(str(port))
            print(response)

class ThriftClient():
    def __init__(self, host, port, service_name):
        self.service = getattr(microservice_thrift, service_name)
        self.client = make_client(self.service, host, port)

    def request(self, api_name, req):
        print self.client._req(api_name, req=req)

if __name__=='__main__':
    client = ThriftClient('127.0.0.1', 1111, "HiService")

    #print microservice_thrift.__dict__.items()
    #print client.__dict__["client"].__dict__.items()

    api_name = "Hi"

    req = getattr(microservice_thrift, "HiRequest")("cc")
    client.request(api_name, req=req)

