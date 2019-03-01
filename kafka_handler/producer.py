from kafka import KafkaProducer
from kafka.errors import KafkaError

from config import *
import json
import msgpack

def on_send_success(record_metadata):
    print "[%s] success, partition:%s, offset:%s " % (record_metadata.topic, record_metadata.partition, record_metadata.offset)

def on_send_error(excp):
    print "[%s] ERROR %s " % (excp)

if type == 1:
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers, retries=5, value_serializer=msgpack.dumps)
    producer.send(topic, {'key': 'value'}).add_callback(on_send_success).add_errback(on_send_error)
else:
    producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
    producer.send(topic, {'key': 'value'}).add_callback(on_send_success).add_errback(on_send_error)

# block until all async messages are sent
producer.flush()




