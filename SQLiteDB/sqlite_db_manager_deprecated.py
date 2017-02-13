from SQLiteDB.SQLiteDB import SQLiteDB
from time import localtime, strftime

class CandleLocationSQL(SQLiteDB):
    def __init__(self, schema, table_name):
        SQLiteDB.__init__(self, schema, table_name)

    def set_db(self, query):
        self.init_db(query)

    def connect_db(self):
        self.con = self.create_connection()
        self.cur = self.con.cursor()

    def insert_data(self, json_data):
        # {'device_id':'test', 'candle_flag':1, 'lat':128.0, 'lng':37.0 }
        query = 'SELECT device_id from {} where device_id="{}"'.format(self._table, json_data['device_id'])
        self.cur.execute(query)
        check_data = self.cur.fetchall()

        if len(check_data) == 0:
            query = 'INSERT INTO {} VALUES ("{}", {}, {}, {})'\
                .format(self._table, json_data['device_id'], json_data['candle_flag'], json_data['lat'], json_data['lng'])
            self.cur.execute(query)
        else:

            query = 'UPDATE {} SET candle_flag={}, lat={}, lng={} WHERE device_id="{}"'\
                .format(self._table, json_data['candle_flag'], json_data['lat'], json_data['lng'], json_data['device_id'])
            self.cur.execute(query)

        self.con.commit()

    def get_candle_flag(self, device_id):
        self.cur.execute('SELECT candle_flag FROM {} WHERE device_id="{}"'.format(self._table, device_id))

        return self.cur.fetchall()


class CandleBoardSQL(SQLiteDB):
    def __init__(self, schema, table_name):
        SQLiteDB.__init__(self, schema, table_name)

    def set_db(self, query):
        self.init_db(query)

    def connect_db(self):
        self.con = self.create_connection()
        self.cur = self.con.cursor()

    def insert_data(self, json_data):
        #query = 'SELECT * from {} WHERE post_date="{}"'.format(self._table, '2016-11-28 10:48:43')
        #self.cur.execute(query)
        #print(self.cur.fetchall())
        post_time_str = strftime('%Y-%m-%d %I:%M:%S', localtime())
        query = 'INSERT INTO {} VALUES ("{}", "{}")'.format(self._table, post_time_str, json_data['content'])
        self.cur.execute(query)
        self.con.commit()

