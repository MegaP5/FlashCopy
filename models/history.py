import sqlite3
from datetime import datetime
import time

class History:
    def __init__(self):
        self.conn = sqlite3.connect('app_data/history.db')
        self.cursor = self.conn.cursor()

        self.create_table_en()

        self.history_position_en = [
        self.history_rows("EN", """SELECT COUNT(*) FROM history_en"""),
        self.history_rows("EN", """SELECT COUNT(*) FROM history_en""")]

    def create_table_en(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS "history_en" (
            "id_word"	INTEGER NOT NULL UNIQUE,
            "word"	VARCHAR(40) NOT NULL,
            "stars"	INTEGER NOT NULL,
            "datetime"	timestamp NOT NULL,
            PRIMARY KEY("id_word")
            )''')
        self.conn.commit()

    def set_history(self, word, stars, language):

        now = datetime.now()
        timestamp = datetime.timestamp(now)
        conn = sqlite3.connect('app_data/history.db')
        cursor = conn.cursor()

        if language == "EN":
            cursor.execute("""INSERT INTO history_en (word, stars, datetime) VALUES (?, ?, ?)""", (word, stars, timestamp))
            conn.commit()
        conn.close()

    def history_get(self, sql_string, language):


        if language == "EN":
            self.cursor.execute(sql_string)
            return self.cursor.fetchall()

    def history_rows(self, language, sql_string):

        conn = sqlite3.connect('app_data/history.db')
        cursor = conn.cursor()

        if language == "EN":
            cursor.execute(sql_string)
            history = cursor.fetchall()[0][0]
            conn.close()
            return history