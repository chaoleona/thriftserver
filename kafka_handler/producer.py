from kafka import KafkaProducer
from kafka.errors import KafkaError

import sys, os
sys.path.insert(0, os.getcwd())
from lib.config import ConfigParser

import json
import msgpack

class MyProducer():
    def __init__(self, conf_file="conf/kafka.conf"):
        parser = ConfigParser(conf_file)
        self.conf = parser.conf["producer"]

        if self.conf["type"] == "1":
            self.producer = KafkaProducer(bootstrap_servers=[self.conf["bootstrap_servers"]], retries=5, value_serializer=msgpack.dumps)
        else:
            self.producer = KafkaProducer(bootstrap_servers=[self.conf["bootstrap_servers"]], retries=5, value_serializer=lambda m: json.dumps(m).encode('ascii'))

    def on_send_success(self, record_metadata):
        print "[%s] success, partition:%s, offset:%s " % (record_metadata.topic, record_metadata.partition, record_metadata.offset)

    def on_send_error(self, excp):
        print "[%s] ERROR %s " % (excp)

    def send(self, msg_data={}, blocked=1):
        self.producer.send(self.conf["topic"], msg_data).add_callback(self.on_send_success).add_errback(self.on_send_error)

        # block until all async messages are sent
        if blocked == 1:
            self.producer.flush()




