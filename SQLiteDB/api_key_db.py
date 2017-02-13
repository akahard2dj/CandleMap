from SQLiteDB.SQLiteDB import SQLiteDB
from time import localtime, strftime
import os
import binascii
import sqlite3


class APIKey(SQLiteDB):
    __db_name = 'apikey.db'
    __table_name = 'api_key'
    __table_query = 'CREATE TABLE {}(issue_date DATETIME, api_key TEXT PRIMARY KEY, status_flag INTEGER)'.format(__table_name)
    status_flag = {'ISSUED': 1, 'DISCARDED': 2}

    def __init__(self):
        SQLiteDB.__init__(self, self.__db_name, self.__table_name)
        self.init_db(self.__table_query)

    def __connect_db(self):
        self.con = self.create_connection()
        self.cur = self.con.cursor()

    def connect(self):
        res = dict()
        try:
            self.__connect_db()
            res['connection_status'] = 'normal'
        except sqlite3.OperationalError:
            res['connection_status'] = 'failed'

        return res

    def issue(self):
        key = binascii.hexlify(os.urandom(24)).decode('utf-8')
        issue_time_str = strftime('%Y-%m-%d %H:%M:%S', localtime())
        query = 'INSERT INTO {} VALUES ("{}", "{}", {})'.format(self._table, issue_time_str, key, self.status_flag['ISSUED'])
        self.cur.execute(query)
        self.con.commit()

    def is_issued_key(self, key):
        query = 'SELECT * FROM {} WHERE api_key="{}"'.format(self._table, key)
        self.cur.execute(query)
        res = self.cur.fetchall()
        if len(res) == 1:
            return True
        else:
            return False
