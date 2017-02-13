import sqlite3
import os


class SQLiteDB:
    def __init__(self, schema, table):
        self._schema = schema
        self._table = table
        self.con = None
        self.cur = None

    def init_db(self, query):
        self.con = self.create_connection()
        self.cur = self.con.cursor()

        if not self.is_table_exists(self._table):
            self.create_table(query)

    def create_connection(self):
        try:
            db_storage = os.path.join(os.getcwd(), self._schema)
            con = sqlite3.connect(db_storage)
        except sqlite3.DatabaseError as e:
            print('{}'.format(e))
            raise
        else:
            return con

    def create_table(self, query):
        query_to_execute = '''{}'''.format(query)
        self.cur.execute(query_to_execute)

    def is_table_exists(self, table_name):
        self.cur.execute("SELECT NAME FROM sqlite_master WHERE TYPE='table' AND NAME='{}'".format(table_name))
        res = list(self.cur)
        if not res:
            return False
        else:
            return True

    def fetch_data(self):
        self.cur.execute("SELECT * FROM {}".format(self._table))

        return self.cur.fetchall()

    def fetch_all(self):
        query = 'SELECT rowid, * FROM {}'.format(self._table)
        self.cur.execute(query)

        return self.cur.fetchall()
