from dbconnection import *


class DbTable:
    dbconn = None

    def __init__(self):
        return

    def table_name(self):
        return self.dbconn.prefix + "table"

    def columns(self):
        return {"test": ["integer", "PRIMARY KEY"]}

    def column_names(self):
        return list(self.columns().keys())

    def primary_key(self):
        res = list(self.columns().keys())
        if 'Country_id' in res:
            return ['Country_id']
        if 'Player_id' in res:
            return ['Player_id']

    def column_names_without_id(self):
        res = list(self.columns().keys())
        if 'Country_id' in res:
            res.remove('Country_id')
        if 'Player_id' in res:
            res.remove('Player_id')
        return res

    def table_constraints(self):
        return []

    def create(self):
        arr = [k + " " + " ".join(v) for k, v in sorted(self.columns().items(), key=lambda x: x[0])]
        sql = f"""CREATE TABLE {self.table_name()}({", ".join(arr + self.table_constraints())})"""
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def drop(self):
        sql = f"""DROP TABLE IF EXISTS {self.table_name()}"""
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def insert_one(self, vals):
        for i in range(0, len(vals)):
            if type(vals[i]) == str:
                vals[i] = "'" + vals[i] + "'"
            else:
                vals[i] = str(vals[i])
        if vals[1] == "''":
            vals[1] = "NULL"
        sql = f"""INSERT INTO {self.table_name()}({", ".join(self.column_names_without_id())}) 
        VALUES({", ".join(vals)})"""
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def delete_one(self, arg):
        sql = f"""DELETE FROM {self.table_name()} 
        WHERE {", ".join(self.primary_key())} 
        = (SELECT {", ".join(self.primary_key())} FROM {self.table_name()} LIMIT 1 OFFSET {arg-1})"""
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def all(self):
        sql = f"""SELECT * FROM {self.table_name()} ORDER BY {", ".join(self.primary_key())}"""
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

