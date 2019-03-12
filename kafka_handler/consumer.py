from kafka import KafkaConsumer
import json
import msgpack

import sys, os
sys.path.insert(0, os.getcwd())
from db.mysql_handler import MySqlHanler
from lib.config import ConfigParser

class MyConsumer():
    def __init__(self, conf_file="conf/kafka.conf"):
        parser = ConfigParser(conf_file)
        self.conf = parser.conf["consumer"]

        print [self.conf["bootstrap_servers"]]

        # To consume latest messages and auto-commit offsets
        if self.conf["type"] == "1":
            value_deserializer = msgpack.unpackb
        else:
            value_deserializer = lambda m: json.loads(m.decode('ascii'))

        self.consumer = KafkaConsumer(self.conf["topic"], group_id=self.conf["group_id"], bootstrap_servers=[self.conf["bootstrap_servers"]],
                                 value_deserializer=value_deserializer, auto_offset_reset='latest',
                                 enable_auto_commit=True)


    def start(self):
        db_handler = MySqlHanler("conf/db_write.conf", "test_db")

        for message in self.consumer:
            # message value and key are raw bytconsumeres -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            print ("%s:%d:%d: value=%s" % (message.topic, message.partition,
                                                      message.offset, message.value))
            db_handler.write_to_mysqlclient(message.value, offset="%d" % (message.offset))
            print "debug ", db_handler.read_by_mysqlclient("ad_bk")

        db_handler.close()

if __name__ == "__main__":
    c = MyConsumer()
    c.start()