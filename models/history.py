import sqlite3
from datetime import datetime
import time

class History:
    def __init__(self):
        self.conn = sqlite3.connect('app_data/history.db')
        self.cursor = self.conn.cursor()

        self.create_table_en()

        self.history_position_en = [self.history_rows("EN"),self.history_rows("EN")]

    def create_table_en(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS "history_en" (
            "id_word"	INTEGER NOT NULL UNIQUE,
            "word"	VARCHAR(40) NOT NULL,
            "stars"	VARCHAR(5) NOT NULL,
            "datetime"	timestamp NOT NULL,
            PRIMARY KEY("id_word")
            )''')
        self.conn.commit()

    def set_history(self, word, stars, language):

        now = datetime.now()
        timestamp = datetime.timestamp(now)

        if language == "EN":
            self.cursor.execute("""INSERT INTO history_en (word, stars, datetime) VALUES (?, ?, ?)""", (word, stars, timestamp))
            self.conn.commit()

    def history_get(self, first, last, language):
        if language == "EN":
            self.cursor.execute("""SELECT * FROM history_en WHERE id_word BETWEEN (?) AND (?) ORDER BY id_word DESC""", (first, last, ))
            return self.cursor.fetchall()

    def history_rows(self, language):
        if language == "EN":
            self.cursor.execute("""SELECT COUNT(*) FROM history_en""")
            return self.cursor.fetchall()[0][0]