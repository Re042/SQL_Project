from dbtable import *


class PlayersTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "Players"

    def columns(self):
        return {"Player_id": ["serial", "PRIMARY KEY"],
                "First_name": ["text", "NOT NULL"],
                "Second_name": ["text", "NOT NULL"],
                "Birthday": ["date", "NOT NULL"],
                "Player_country_id": ["integer", "NOT NULL"]}

    def table_constraints(self):
        return ["FOREIGN KEY(player_country_id) REFERENCES Countries(country_id) ON DELETE CASCADE"]

    def all_by_country_id(self, pid):
        sql = f"""SELECT * FROM {self.table_name()} WHERE Player_country_id = {str(pid)} 
        ORDER BY {", ".join(self.primary_key())}"""
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def find(self, num1, num2):
        sql = f"""SELECT * FROM {self.table_name()} WHERE Player_country_id = {num1} 
        LIMIT 1 OFFSET {num2-1}"""
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()
