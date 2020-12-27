import sqlite3

class Dictionary:
    def __init__(self):
        self.conn = sqlite3.connect('app_data/dictionary.db')
        self.cursor = self.conn.cursor()
        self.create_dictionary_table()
        self.set_default_settings()

    def create_dictionary_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS "dict_jp" (
            "name"	VARCHAR(30) NOT NULL,
            "type"	VARCHAR(5) NOT NULL,
            "src"	TEXT NOT NULL
            )''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS "dict_en" (
            "name"	VARCHAR(30) NOT NULL,
            "type"	VARCHAR(5) NOT NULL,
            "src"	TEXT NOT NULL
            )''')
        self.conn.commit()

            

    def set_default_settings(self):
        self.cursor.execute ("""SELECT * FROM dict_jp""")
        if self.cursor.fetchone():
            return
        else:
            self.cursor.execute("""INSERT INTO dict_jp (name, type, src) VALUES ("Jisho (JP)", "web", "https://jisho.org/search/{word}")""")
            self.cursor.execute("""INSERT INTO dict_jp (name, type, src) VALUES ("Goo (JP)", "web", "https://dictionary.goo.ne.jp/srch/all/{word}/m0u/")""")
            self.cursor.execute("""INSERT INTO dict_jp (name, type, src) VALUES ("Weblio (JP)", "web", "https://www.weblio.jp/content/{word}")""")
            self.cursor.execute("""INSERT INTO dict_en (name, type, src) VALUES ("Cambridge (EN)", "web", "https://dictionary.cambridge.org/pt/dicionario/ingles/{word}")""")
            self.cursor.execute("""INSERT INTO dict_en (name, type, src) VALUES ("Dictionary (EN)", "web", "https://www.dictionary.com/browse/{word}?s=t")""")
            self.cursor.execute("""INSERT INTO dict_en (name, type, src) VALUES ("Google Translate (EN > PT-BR)", "web", "https://translate.google.com.br/?hl=pt-BR&tab=wT&sl=en&tl=pt&text={word}%0A&op=translate")""")
            self.cursor.execute("""INSERT INTO dict_en (name, type, src) VALUES ("Linguee (EN > PT-BR)", "web", "https://www.linguee.com.br/portugues-ingles/search?source=ingles&query={word}")""")
            self.cursor.execute("""INSERT INTO dict_en (name, type, src) VALUES ("Oxford Languages (EN)", "web", "https://www.google.com/search?source=hp&ei=9XPIX6uZB4C05OUPpOO80AY&q=definition {word}")""")
            self.conn.commit()


    def get_url(self, name, language):
        conn = sqlite3.connect('app_data/dictionary.db')
        cursor = conn.cursor()
        if language == "JP":
            cursor.execute("""SELECT * FROM dict_jp WHERE name=(?)""", (name, ))
        elif language == "EN":
            cursor.execute("""SELECT * FROM dict_en WHERE name=(?)""", (name, ))

        url = cursor.fetchall()[0][2]
        conn.close()
        print(url)

        return url