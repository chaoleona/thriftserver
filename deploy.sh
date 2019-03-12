cd /Users/caolihong/MyTest/kafka_2.11-2.1.1

nohup bin/zookeeper-server-start.sh config/zookeeper.properties &

# conf/kafka.conf中 bootstrap_servers = 127.0.0.1:9092
# config/server.properties中设置   listeners=PLAINTEXT://127.0.0.1:9092
nohup bin/kafka-server-start.sh config/server.properties &

#bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic testtopic


