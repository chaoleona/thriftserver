from kafka import KafkaConsumer
from config import *
import json
import msgpack

# To consume latest messages and auto-commit offsets
if type == 1:
    value_deserializer = msgpack.unpackb
else:
    value_deserializer = lambda m: json.loads(m.decode('ascii'))

consumer = KafkaConsumer(topic, group_id=group_id, bootstrap_servers=bootstrap_servers,
                         value_deserializer=value_deserializer, auto_offset_reset='earliest',
                         enable_auto_commit=False)

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))


