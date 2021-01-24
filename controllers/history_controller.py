import time

from models.history import History

class HistoryController:
    def __init__(self):

        self.history = History()
        self.history.create_table_en()        
        self.history_position_en = [self.get_rows("EN", "last", "-"),self.get_rows("EN", "last", "-")]

    def history_show(self, position, sort, word_filter):

        rows = self.history.history_get(self.history_sql_string(position, sort, word_filter), "EN")

        text = ""

        for row in rows:
            text = f'<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:12pt;">{row[1]}</span><span style=" font-size:10pt; color:#cccf00;">{self.stars_show(row[2])}</span><span style=" font-size:10pt;"> </span><span style=" font-size:10pt; color:#8b8b8b;">{time.ctime(row[3])}</span></p><hr/>' + text
        return text

    def get_rows(self, language, sort, word_filter):

        stars_number = 0
        
        if word_filter != None:
            for w in word_filter:
                if w == "★":
                    stars_number += 1

        if word_filter != "-":
            filter_string = f"WHERE stars ='{stars_number}' "
        else:
            filter_string = ""

        word_order = ""

        if sort == "last":
            word_order = "DESC"

        sql_string = f"""SELECT COUNT(*) FROM history_en {filter_string} ORDER BY id_word {word_order}"""

        return self.history.history_rows(language, sql_string)

    def set_history(self, word, stars, language):
        self.history.set_history(word, stars, language)

    def stars_show(self, stars):

        stars_list = ["☆☆☆☆☆", '★☆☆☆☆', '★★☆☆☆', '★★★☆☆', '★★★★☆', '★★★★★']

        if type(stars) == int:
            try:
                strs = stars_list[stars]
                return strs
            except:
                return stars_list[0]
        else:
            return stars_list[0]

    def history_sql_string(self, position, sort, word_filter):
        
        first = position - 50

        if first < 0:
            first = 0

        stars_number = 0
        
        if word_filter != None:
            for w in word_filter:
                if w == "★":
                    stars_number += 1

        if word_filter != "-":
            filter_string = f" WHERE stars='{stars_number}'"
        else:
            filter_string = ""

        word_order = ""

        if sort == "first":
            word_order = "DESC"

        sql_string = f"""SELECT * FROM history_en{filter_string} ORDER BY id_word {word_order} LIMIT 50 OFFSET {first}"""

        
        return sql_string