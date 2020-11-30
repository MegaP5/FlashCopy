import time

from models.history import History

class HistoryController:
    def __init__(self):

        self.history = History()
        self.history.create_table_en()        
        self.history_position_en = [self.get_rows("EN"),self.get_rows("EN")]
    
    def history_show(self, position):

        text = ""
        first = position - 50

        if first < 0:
            first = 0

        rows = self.history.history_get(first, position, "EN")

        for row in rows:
            text = text + f'<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:12pt;">{row[1]}</span><span style=" font-size:10pt; color:#cccf00;">{self.stars_show(row[2])}</span><span style=" font-size:10pt;"> </span><span style=" font-size:10pt; color:#8b8b8b;">{time.ctime(row[3])}</span></p><hr/>'
        return text

    def get_rows(self, language):
        return self.history.history_rows(language)

    def set_history(self, word, stars, language):
        self.history.set_history(word, stars, language)

    def stars_show(self, stars):
        stars_list = ["☆☆☆☆☆", '★☆☆☆☆', '★★☆☆☆', '★★★☆☆', '★★★★☆', '★★★★★']
        return stars_list[stars]