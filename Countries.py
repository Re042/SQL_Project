from dbtable import *


class CountriesTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "Countries"

    def columns(self):
        return {"Country_id": ["serial", "PRIMARY KEY"],
                "Short_name": ["text", "NOT NULL"],
                "Long_name": ["text"],
                "Region": ["text", "NOT NULL"]}

    def table_constraints(self):
        return ["UNIQUE (Short_name), UNIQUE (Long_name)"]

    def find(self, num):
        sql = f"""SELECT * FROM {self.table_name()} LIMIT 1 OFFSET {num-1}"""
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()

    def find_by_short_name(self, sh):
        sql = f"""SELECT * FROM {self.table_name()} WHERE short_name = '{sh}'"""
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def find_by_long_name(self, lg):
        sql = f"""SELECT * FROM {self.table_name()} WHERE long_name = '{lg}'"""
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()
