from kafka import SimpleClient

hosts = "127.0.0.1:9092"
client = SimpleClient(hosts=hosts)
print client.topics




