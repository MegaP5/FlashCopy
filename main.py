from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic, QtCore
from PyQt5.Qt import *
from PyQt5.QtWebEngineWidgets import *

import tkinter
import sys
import unicodedata
import importlib

import app_data.verb_maker.japanese.main as desc
import app_data.frequency.frequency as frequency

# CONTROLLERS
from controllers.card_maker_controller import CardMakerController
from controllers.dictionary_controller import DictionaryController
from controllers.history_controller import HistoryController
from controllers.settings_controller import SettingsController


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("views/app.ui", self)

        # CONTROLLERS
        self.card_maker = CardMakerController()
        self.dictionary = DictionaryController()
        self.history = HistoryController()
        self.settings = SettingsController()

        # HISROTY
        self.history.history_position_en[0] = self.history.get_rows("EN")
        self.history_en.setText(self.history.history_show(self.history.get_rows("EN")))
        self.next_button.clicked.connect(self.history_next)
        self.prev_button.clicked.connect(self.history_prev)

        if(self.history.get_rows("EN") <= 50):
            self.next_button.setEnabled(False)

        # CONFIGS
        self.settings_list = self.settings.get_settings()

        # DICTIONARY
        self.cm_jp.addItems(self.dictionary.get_dict_list_jp())
        self.cm.addItems(self.dictionary.get_dict_list_en())

        # LOAD THE DEFAULT DICTIONARY
        try:
            self.jp_dict = importlib.import_module("app_data.dictionary.JP." + self.settings_list[0][1] + ".main")
            self.en_dict = importlib.import_module("app_data.dictionary.EN." + self.settings_list[0][3] + ".main")
        except ModuleNotFoundError:
            print("Dictionary not found")


        # SET SETTINGS VALUES
        index0 = self.jp_dic.findText(self.settings_list[0][0], QtCore.Qt.MatchFixedString)
        self.jp_dic.setCurrentIndex(index0)

        index1 = self.cm_jp.findText(self.settings_list[0][1], QtCore.Qt.MatchFixedString)
        self.cm_jp.setCurrentIndex(index1)

        index2 = self.dic.findText(self.settings_list[0][2], QtCore.Qt.MatchFixedString)
        self.dic.setCurrentIndex(index2)

        index3 = self.cm.findText(self.settings_list[0][3], QtCore.Qt.MatchFixedString)
        self.cm.setCurrentIndex(index3)

        # SAVE VALUES ON DB
        self.save_cfg.clicked.connect(self.save_configs)
        self.dict_web.load(QUrl("https://dictionary.cambridge.org/pt/"))
        self.save_card.clicked.connect(self.save_card_clicked)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)     

        QApplication.clipboard().dataChanged.connect(self.clipboardChanged)
        self.show()

        # ABOUT
        self.textBrowser.setOpenExternalLinks(True)


    def save_card_clicked(self):

        # SAVE CARD
        self.card_maker.s_card()
        # TURN OFF THE SAVE BUTTON
        self.save_card.setEnabled(False)


    def save_configs(self):

        #SAVE ALL SETTINGS
        self.settings.set_settings(
        self.jp_dic.currentText(), 
        self.cm_jp.currentText(), 
        self.dic.currentText(), 
        self.cm.currentText())


    def update_gui(self, word, b_card, tag, stars, language):

        url = self.dictionary.get_dict_url(language, word)
        self.dict_web.load(QUrl(url))           
        self.front_card.setText(word)
        self.back_card.setText(f"<center><br/><h2>{stars}<h2></center>{b_card}")
        self.tag_card.setText(tag)
        self.strs.setText(f"<html><head/><body><p><span style=' color:#f0d342;'>{stars}</span></p></body></html>")

        self.card_maker.front = word
        self.card_maker.back = b_card
        self.card_maker.tag = tag
        self.card_maker.stars = stars
        if language == "EN":
            self.card_maker.deck = [language, self.settings_list[0][3]]
        elif language == "JP":
            self.card_maker.deck = [language, self.settings_list[0][1]]


    def gui_clean(self):

        self.save_card.setEnabled(True)
        self.front_card.setText(self.card_maker.front)
        self.back_card.setText(f"<center><br/><h2>{self.stars}<h2></center>{self.card_maker.back}")
        self.tag_card.setText(self.card_maker.tag)
        self.strs.setText(f"<html><head/><body><p><span style=' color:#f0d342;'>{self.card_maker.stars}</span></p></body></html>")


    def clipboardChanged(self):

        #q_text = QApplication.clipboard().text()
        self.focusOutEvent(QApplication)

        try:    
            text = tkinter.Tk().clipboard_get().lower().strip()
        except tkinter.TclError:
            text = None

        if type(text) == str:            
            if unicodedata.category(text[0]) == "Lo":

                self.card_maker.inf_clean()
                word_desc = desc.r_conj(text)
                definitions = self.jp_dict.main(word_desc)
                stars = frequency.f_stars("JP", word_desc)

                b_card = ""

                for wo in definitions:
                    b_card = b_card + f"<center>{wo[5][0]}</center>"

                self.update_gui(word_desc, b_card, word_desc, stars, "JP")


            elif " " in text:

                self.card_maker.inf_clean()
                self.gui_clean()
                self.dict_web.load(QUrl(f"https://translate.google.com.br/?hl=pt-BR&tab=TT&sl=auto&tl=pt&text={text}&op=translate"))

            else:

                self.card_maker.inf_clean()
                stars = frequency.f_stars("EN", text)
                ba_card = self.en_dict.main(text)

                f_card = text.replace('\n', '')

                b_card = []
                for b in ba_card:              
                    b_card.append(b.replace('\n', ''))

                t_card = f_card

                self.update_gui(f_card, b_card[0], t_card, stars, "EN")
                if f_card != self.card_maker.last_word:
                    self.history.set_history(f_card, stars, "EN")
                    self.card_maker.last_word = text

                self.history.history_position_en[0] = self.history.get_rows("EN")
                self.prev_button.setEnabled(False)
                if(self.history.get_rows("EN") <= 50):
                    self.next_button.setEnabled(False)                
                self.history_en.setText(self.history.history_show(self.history.get_rows("EN")))
                self.save_card.setEnabled(True)


    def closeEvent(self, event):
        event.accept()

    def focusOutEvent(self, event):
        self.setWindowState(window.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.activateWindow()
        self.raise_()


    def history_prev(self):
         
        self.history.history_position_en[0] = self.history.history_position_en[0] + 50

        if(self.history.history_position_en[0] >= self.history.get_rows("EN")):
            self.history.history_position_en[0] = self.history.get_rows("EN")
            self.prev_button.setEnabled(False)

        if self.history.history_position_en[0] - 50 >= 0:
            self.next_button.setEnabled(True)
        else:
            self.next_button.setEnabled(False)

        self.history_en.setText(self.history.history_show(self.history.history_position_en[0]))

    def history_next(self):

        self.history.history_position_en[0] = self.history.history_position_en[0] - 50

        if self.history.history_position_en[0] <= 50:
            self.next_button.setEnabled(False)

        if self.history.history_position_en[0] <= 0:
            self.history.history_position_en[0] = 0

        if self.history.history_position_en[0] + 50 >= self.history.get_rows("EN"):
            self.prev_button.setEnabled(True)
        else:
            self.prev_button.setEnabled(True)

        self.history_en.setText(self.history.history_show(self.history.history_position_en[0]))

    
app = QApplication(sys.argv)

web = QWebEngineView()

icon = QIcon("content/icon.ico")

tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)


menu = QMenu()

quit = QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)

tray.setContextMenu(menu)

window = UI()
app.exec_()