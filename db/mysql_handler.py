import MySQLdb
from profilehooks import profile

import sys, os
sys.path.insert(0, os.getcwd())

from lib.config import ConfigParser


class MySqlHanler:
    def __init__(self, conf_file="conf/db.conf", db_name="test_db"):
        parser = ConfigParser(conf_file)
        conf = parser.conf[db_name]

        self.conn = MySQLdb.connect(host=conf["host"], user=conf["user"], password=conf["password"], db=conf["db_name"])
        self.cursor = self.conn.cursor()
        self.update_cnt = 0

    #@profile(immediate=False)
    def read_by_mysqlclient(self, table_name="ad"):
        self.cursor.execute("select * from " + table_name + ";")
        res = self.cursor.fetchone()
        return res

    #@profile(immediate=True)
    def write_to_mysqlclient(self, data, table_name="ad_bk", offset=0):
        try:
            self.update_cnt = int(offset)
            name = data["name"] + "_" + offset
            id_t = data["task_id"]
            cmd = "update " + table_name + " set name=\"" + name + "\" where id=" + str(id_t) + ";"
            self.cursor.execute(cmd)
            self.conn.autocommit(True)
        except Exception,e:
            print e.__str__()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    db_handler = MySqlHanler()
    db_handler.read_by_mysqlclient()
    db_handler.close()