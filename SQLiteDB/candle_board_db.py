from SQLiteDB.SQLiteDB import SQLiteDB
from time import localtime, strftime
import sqlite3


class CandleBoard(SQLiteDB):
    __db_name = 'candle_board.db'
    __table_query = 'CREATE TABLE candle_board(post_date DATETIME PRIMARY KEY, content TEXT, status_flag INTEGER)'
    flag_dict = {'POST': 1, 'DELETE': 2}

    def __init__(self):
        SQLiteDB.__init__(self, self.__db_name, 'candle_board')
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

    def db_update(self, flag, json_data):
        # flag = 1 post
        # flag = 2 delete
        #flag_dict = {'POST': 1, 'DELETE': 2}
        if flag == 1:
            #self.db.insert_data(json_data)
            post_time_str = strftime('%Y-%m-%d %H:%M:%S', localtime())
            query = 'INSERT INTO {} VALUES ("{}", "{}", {})'.format(self._table, post_time_str, json_data['content'], self.flag_dict['POST'])
            self.cur.execute(query)
            self.con.commit()
        if flag == 2:
            query = 'UPDATE {} SET status_flag={} WHERE rowid={}'.format(self._table, self.flag_dict['DELETE'], json_data['rowid'])
            self.cur.execute(query)
            self.con.commit()

    def fetch_posted(self):
        query = 'SELECT rowid, * from {} where status_flag={}'.format(self._table, self.flag_dict['POST'])
        self.cur.execute(query)
        return self.cur.fetchall()

    def fetch_posted_step(self, offset, limit):
        query = 'SELECT rowid, post_date, content from {} where status_flag={} ORDER BY rowid DESC LIMIT {} OFFSET {}'.format(self._table, self.flag_dict['POST'], limit, offset)
        self.cur.execute(query)
        res = self.cur.fetchall()
        output = list()
        for item in res:
            item_dict = dict()
            item_dict['id'] = item[0]
            item_dict['date'] = item[1]
            item_dict['content'] = item[2]
            output.append(item_dict)
        return output
