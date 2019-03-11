# coding:utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_ERROR
import datetime
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log/run_time_log.txt',
                    filemode='a')

def increment_reload_db(args):
    """
    定时查看数据库更新信息，并发给kafka
    :param args:
    :return:
    """
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    

def my_listener(event):
    """
    监听循环任务的EVENT_JOB_ERROR事件的处理函数，打印错误日志
    :param event: ERROR事件
    :return:
    """
    if event.exception:
        print 'increment_reload_db Task Run ERROR ！Information: [', event.exception, ']'

scheduler = BlockingScheduler()
scheduler.add_job(func=increment_reload_db, args=('循环任务',), trigger='interval', seconds=2, id='increment_reload_db_task')
scheduler.add_listener(my_listener, EVENT_JOB_ERROR)

scheduler._logger = logging

scheduler.start()
