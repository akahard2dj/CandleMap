from SQLiteDB.SQLiteDB import SQLiteDB
from time import localtime, strftime
import sqlite3


class CandleCount(SQLiteDB):
    __db_name = 'candle_count.db'
    __table_query = 'CREATE TABLE candle_count(query_date DATETIME PRIMARY KEY, candle_count INTEGER)'

    def __init__(self):
        SQLiteDB.__init__(self, self.__db_name, 'candle_count')
        self.init_db(self.__table_query)
        self.init_candle = 162


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

    def db_update(self, json_data):
        candle_query_date = strftime('%Y-%m-%d', localtime())

        query = 'SELECT query_date from {} where query_date="{}"'.format(self._table, candle_query_date)
        self.cur.execute(query)
        check_data = self.cur.fetchall()
        if len(check_data) == 0:
            query = 'INSERT INTO {} VALUES ("{}", {})'.format(self._table, candle_query_date, self.init_candle)
            self.cur.execute(query)
            self.con.commit()

        else:
            query = 'SELECT candle_count from {} WHERE query_date="{}"'.format(self._table, candle_query_date)
            self.cur.execute(query)
            res = self.cur.fetchall()
            count = res[0][0]
            count += json_data['count']

            query = 'UPDATE {} SET candle_count={} WHERE query_date="{}"' \
                .format(self._table, count, candle_query_date)
            self.cur.execute(query)
            self.con.commit()

    def get_candle_count(self):
        candle_query_date = strftime('%Y-%m-%d', localtime())
        query = 'SELECT candle_count from {} WHERE query_date="{}"'.format(self._table, candle_query_date)
        self.cur.execute(query)
        res = self.cur.fetchall()

        if not res:
            count = self.init_candle
        else:
            count = res[0][0]

        return count
