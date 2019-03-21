# coding:utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_ERROR
import datetime
import logging

import sys, os
sys.path.insert(0, os.getcwd())

from db.mysql_handler import MySqlHanler
from kafka_handler.producer import MyProducer

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log/run_time_log.txt',
                    filemode='a')

db_handler = MySqlHanler()
producer = MyProducer()

def increment_reload_db(args):
    """
    定时查看数据库更新信息，并发给任务给kafka
    :param args:
    :return:
    """
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    res = db_handler.read_by_mysqlclient()
    res_one = res

    msg_data = {"task_id":res_one[0], "name":res_one[1]}
    producer.send(msg_data)

    db_handler.close()

increment_reload_db("")
