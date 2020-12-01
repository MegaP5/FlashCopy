import sqlite3

class Settings:
    def __init__(self):
        self.conn = sqlite3.connect('app_data/settings.db')
        self.cursor = self.conn.cursor()

    def create_settings_table(self):
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS "settings" (
                "dict_jp"	VARCHAR(30) NOT NULL UNIQUE,
                "cm_jp"	VARCHAR(30) NOT NULL UNIQUE,
                "dict_en"	VARCHAR(30) NOT NULL UNIQUE,
                "cm_en"	VARCHAR(30) NOT NULL UNIQUE,
                "theme"	VARCHAR(30) NOT NULL UNIQUE
                )''')  
        except sqlite3.Error as error:
            print("Update sqlite error", error)


    def create_user(self):
        self.cursor.execute ("""SELECT * FROM settings""")
        if self.cursor.fetchone():
            return
        else:
            self.cursor.execute("""INSERT INTO settings (dict_jp, cm_jp, dict_en, cm_en, theme) 
            VALUES ("Jisho (JP)", "None", "Cambridge (EN)", "None", "ManjaroMix")""")
            self.conn.commit()


    def get_settings(self):
        self.cursor.execute("""SELECT * FROM settings""")
        return self.cursor.fetchall()

    def set_settings(self, dict_jp, cm_jp, dict_en, cm_en, theme):
        self.cursor.execute("""DELETE FROM settings""")
        self.cursor.execute("""INSERT INTO settings (dict_jp, cm_jp, dict_en, cm_en, theme) 
        VALUES (?, ?, ?, ?, ?)""", (dict_jp, cm_jp, dict_en, cm_en, theme))
        self.conn.commit()