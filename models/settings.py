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

        
    def create_hotkeys_table(self):
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS "hotkeys" (
                "auto_fill"	VARCHAR(30) NOT NULL,
                "set_front"	VARCHAR(30) NOT NULL,
                "set_back"	VARCHAR(30) NOT NULL,
                "set_tag"	VARCHAR(30) NOT NULL
                )''')  
        except sqlite3.Error as error:
            print("Update sqlite error", error)


    def create_user(self):
        self.cursor.execute ("""SELECT * FROM settings""")
        if not self.cursor.fetchone():
            self.cursor.execute("""INSERT INTO settings (dict_jp, cm_jp, dict_en, cm_en, theme) 
            VALUES ("Jisho (JP)", "None", "Cambridge (EN)", "None", "ManjaroMix")""")
            self.conn.commit()


    def create_default_hotkeys(self):
        self.cursor.execute ("""SELECT * FROM hotkeys""")
        if not self.cursor.fetchone():
            self.cursor.execute("""INSERT INTO hotkeys (auto_fill, set_front, set_back, set_tag) 
            VALUES ("<ctrl>+1", "<ctrl>+2", "<ctrl>+3", "<ctrl>+4")""")
            self.conn.commit()


    def get_settings(self):
        conn = sqlite3.connect('app_data/settings.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM settings""")
        settings = cursor.fetchall()
        conn.close()
        return settings


    def get_hotkeys(self):
        conn = sqlite3.connect('app_data/settings.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM hotkeys""")
        hotkeys = cursor.fetchall()
        conn.close()
        return hotkeys


    def set_settings(self, dict_jp, cm_jp, dict_en, cm_en, 
    theme, fill_key_a, fill_key_b, front_key_a, 
    front_key_b, back_key_a, back_key_b, tag_key_a, 
    tag_key_b):

        self.cursor.execute("""DELETE FROM settings""")
        self.cursor.execute("""INSERT INTO settings (dict_jp, cm_jp, dict_en, cm_en, theme) 
        VALUES (?, ?, ?, ?, ?)""", (dict_jp, cm_jp, dict_en, cm_en, theme))
        self.conn.commit()
        self.cursor.execute("""DELETE FROM hotkeys""")
        self.cursor.execute("""INSERT INTO hotkeys (auto_fill, set_front, set_back, set_tag) 
        VALUES (?, ?, ?, ?)""", (
        self.make_hotkey(fill_key_a, fill_key_b), self.make_hotkey(front_key_a, front_key_b), 
        self.make_hotkey(back_key_a, back_key_b), self.make_hotkey(tag_key_a, tag_key_b)))
        self.conn.commit()


    def make_hotkey(self, key_a, key_b):

        hotkey = ""

        if key_a == "ctrl":
            hotkey = "<ctrl>+" + str(key_b)            
        elif key_a == "alt":
            hotkey = "<alt>+" + str(key_b)
        elif key_a == "shift":
            hotkey = "<shift>+" + str(key_b)
        elif key_a == "-":
            hotkey = str(key_b)

        return hotkey