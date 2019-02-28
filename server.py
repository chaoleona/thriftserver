#coding=utf-8

import thriftpy
from zookclient import ZookClient
from thriftpy.rpc import make_server

thrift_file = "hi.thrift"
module_name = "hi_thrift"

microservice_thrift = thriftpy.load(thrift_file, module_name=module_name)

class Dispatcher(object):
    def Hi(self, args):
        name = args.Name
        resp = getattr(microservice_thrift, "HiResponse")(Resp="Your Name is " + name)

        print "doReponse! ", args.Name, resp
        return resp

class RpcServer():
    def __init__(self,host,port,appname,zookhost):
        self.port=port
        self.host=host
        self.appname=appname
        self.zookhost=zookhost
    def startServer(self):
        server = make_server(microservice_thrift.MicroService, Dispatcher(),
                             self.host, self.port)
        client=ZookClient(hosts=self.zookhost)
        client.register(self.appname, self.port, self.host)
        server.serve()#启动服务

class ThriftServer():
    def __init__(self, host, port, handler, service_name):
        self.service = getattr(microservice_thrift, service_name)
        self.server = make_server(self.service, handler, host, port)

    def startServer(self):
        self.server.serve()

if __name__=='__main__':
    handler = Dispatcher()
    server = ThriftServer('127.0.0.1', 1111, handler, "HiService")

    #print microservice_thrift.__dict__.items()
    #print server.__dict__["server"].__dict__.items()

    server.startServer()

