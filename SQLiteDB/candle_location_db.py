from SQLiteDB.SQLiteDB import SQLiteDB
from time import localtime, strftime


class CandleLocation(SQLiteDB):
    __db_name = 'candle_location.db'
    __table_query = 'CREATE TABLE candle_location(' \
                    'device_id TEXT PRIMARY KEY, ' \
                    'candle_flag INTEGER, ' \
                    'lat REAL, ' \
                    'lng REAL, ' \
                    'ignition_date DATETIME )'

    def __init__(self):
        SQLiteDB.__init__(self, self.__db_name, 'candle_location')
        self.init_db(self.__table_query)

    def __connect_db(self):
        self.con = self.create_connection()
        self.cur = self.con.cursor()

    def connect(self):
        self.__connect_db()

    def db_update(self, json_data):
        #self.db.insert_data(json_data)
        # {'device_id':'test', 'candle_flag':1, 'lat':128.0, 'lng':37.0 }
        query = 'SELECT device_id from {} where device_id="{}"'.format(self._table, json_data['device_id'])
        self.cur.execute(query)
        check_data = self.cur.fetchall()
        ignition_date_str = strftime('%Y-%m-%d %H:%M:%S', localtime())

        if len(check_data) == 0:
            query = 'INSERT INTO {} VALUES ("{}", {}, {}, {}, "{}")' \
                .format(self._table,
                        json_data['device_id'], json_data['candle_flag'], json_data['lat'], json_data['lng'],
                        ignition_date_str)
            self.cur.execute(query)
        else:
            query = 'UPDATE {} SET candle_flag={}, lat={}, lng={} WHERE device_id="{}"' \
                .format(self._table, json_data['candle_flag'], json_data['lat'], json_data['lng'],
                        json_data['device_id'])
            self.cur.execute(query)

        self.con.commit()

    def get_candle_flag(self, json_data):
        self.cur.execute('SELECT candle_flag FROM {} WHERE device_id="{}"'.format(self._table, json_data['device_id']))
        res = self.cur.fetchall()
        return res[0][0]
