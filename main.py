from PyQt5 import uic, QtCore
from PyQt5.Qt import Qt, QIcon, QSystemTrayIcon, QMenu, QAction, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMainWindow

import random
import sys
import tkinter
import importlib
import requests
from bs4 import BeautifulSoup

# CONTROLLERS
from controllers.card_maker_controller import CardMakerController
from controllers.dictionary_controller import DictionaryController
from controllers.history_controller import HistoryController
from controllers.settings_controller import SettingsController
from controllers.keyboard_controller import KeyboardController


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("views/app.ui", self)


        # CONTROLLERS
        self.card_maker = CardMakerController()
        self.dictionary = DictionaryController()
        self.history = HistoryController()
        self.settings = SettingsController()
        self.keyboard = KeyboardController()

        #KEYBOARD   
        self.keyboard.start()
        self.keyboard.front_value.connect(self.set_front)        
        self.keyboard.back_value.connect(self.set_back)
        self.keyboard.tag_value.connect(self.set_tag)
        self.keyboard.auto_fill.connect(self.update_gui)       

        # HISTORY
        self.history.history_position_en[0] = self.history.get_rows("EN", "last", "-")        
        self.history_en.setText(
        self.history.history_show(
        self.history.history_position_en[0],
        self.sort_box.currentText(), 
        self.filter_box.currentText()))
        self.history_button.clicked.connect(
        self.history_settings_get)
        self.next_button.clicked.connect(
        self.history_next)
        self.prev_button.clicked.connect(
        self.history_prev)

        if(self.history.history_position_en[0] <= 50):
            self.next_button.setEnabled(False)

        # DICTIONARY
        self.cm_jp.addItems(
        self.dictionary.get_dict_list_jp())
        self.cm.addItems(
        self.dictionary.get_dict_list_en())        

        # SETTINGS
        self.settings_list = self.settings.get_settings()

        # SET SETTINGS VALUES
        index0 = self.jp_dic.findText(
        self.settings_list[0][0], QtCore.Qt.MatchFixedString)
        self.jp_dic.setCurrentIndex(index0)

        index1 = self.cm_jp.findText(
        self.settings_list[0][1], QtCore.Qt.MatchFixedString)
        self.cm_jp.setCurrentIndex(index1)

        index2 = self.dic.findText(
        self.settings_list[0][2], QtCore.Qt.MatchFixedString)
        self.dic.setCurrentIndex(index2)

        index3 = self.cm.findText(
        self.settings_list[0][3], QtCore.Qt.MatchFixedString)
        self.cm.setCurrentIndex(index3)

        index4 = self.theme_box.findText(
        self.settings_list[0][4], QtCore.Qt.MatchFixedString)
        self.theme_box.setCurrentIndex(index4)

        # HOTKEYS
        self.hotkeys = self.hotkeys_list(self.settings.get_hotkeys_list())

        self.fill_key_b.setMaxLength(1)
        self.front_key_b.setMaxLength(1)
        self.back_key_b.setMaxLength(1)
        self.tag_key_b.setMaxLength(1)

        # SET SETTINGS HOTKEYS VALUES
        index0 = self.fill_key_a.findText(
        self.hotkeys[0][0], QtCore.Qt.MatchFixedString)
        self.fill_key_a.setCurrentIndex(index0)

        index1 = self.front_key_a.findText(
        self.hotkeys[1][0], QtCore.Qt.MatchFixedString)
        self.front_key_a.setCurrentIndex(index1)

        index2 = self.back_key_a.findText(
        self.hotkeys[2][0], QtCore.Qt.MatchFixedString)
        self.back_key_a.setCurrentIndex(index2)

        index3 = self.tag_key_a.findText(
        self.hotkeys[3][0], QtCore.Qt.MatchFixedString)
        self.tag_key_a.setCurrentIndex(index3)

        self.fill_key_b.setText(self.hotkeys[0][1])
        self.front_key_b.setText(self.hotkeys[1][1])
        self.back_key_b.setText(self.hotkeys[2][1])
        self.tag_key_b.setText(self.hotkeys[3][1])

        # DEFAULT THEME
        self.setStyleSheet(open('content/themes/' + 
        self.theme_box.currentText() + '.css').read())

        # SAVE VALUES ON DB
        self.save_cfg.clicked.connect(
        self.save_configs)
        self.dict_web.load(QUrl("https://dictionary.cambridge.org/pt/"))
        self.save_card.clicked.connect(
        self.save_card_clicked)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)     

        self.show()

        # ABOUT
        self.about_text.setOpenExternalLinks(True)


        self.bold_button_front.clicked.connect(
        self.get_selection)



    def hotkeys_list(self, hotkeys):

        hk = []

        for hotkey in hotkeys[0]:
            if "ctrl" in hotkey:
                hk.append(["ctrl", hotkey[-1]])
            elif "alt" in hotkey:
                hk.append(["alt", hotkey[-1]])
            elif "shift" in hotkey:
                hk.append(["shift", hotkey[-1]])
            else:
                hk.append(["-", hotkey[-1]])

        return hk


    def get_selection(self):
        cursor = self.front_card.textCursor()
        text = self.front_card.toPlainText()
        textSelected = cursor.selectedText()

        #cursor.setPosition(5)
        
        selection_start = cursor.selectionStart()
        selection_end = cursor.selectionEnd()
        
        #s = textSelected.upper()
        #self.about_text.append(s)
        #textSelected.setPosition("uiui", QtGui.QTextCursor.KeepAnchor)

        bold_string = self.bold_string(text, selection_start, selection_end)

        self.front_card.setPlainText(bold_string)


    def bold_string(self, string, selection_start, selection_end):

        if not(selection_start == selection_end):
            string = string[:selection_end] + "</b>" + string[selection_end:]
            string = string[:selection_start] + "<b>" + string[selection_start:]        

        return string


    def set_tag(self, val):
        self.tag_card.setText(val)


    def set_back(self, val):
        self.back_card.setText(val)


    def set_front(self, val):
        self.front_card.setPlainText(val)


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
        self.cm.currentText(),
        self.theme_box.currentText(),
        self.fill_key_a.currentText(),
        self.fill_key_b.text(),
        self.front_key_a.currentText(),
        self.front_key_b.text(),
        self.back_key_a.currentText(),
        self.back_key_b.text(),
        self.tag_key_a.currentText(),
        self.tag_key_b.text())

        self.setStyleSheet(open('content/themes/' + 
        self.theme_box.currentText() + '.css').read())


    def update_gui(self, word, b_card, tag, stars, language):

        self.focusOutEvent(QApplication)

        url = self.dictionary.get_dict_url(language, word)

        self.dict_web.load(QUrl(url))
        self.front_card.setPlainText(word)

        self.back_card.setText(
        f"<center><br/><h2>{self.history.stars_show(stars)}<h2></center>{b_card}")
        
        self.tag_card.setText(tag)

        self.strs.setText(
        f"<html><head/><body><p><span style=' color:#f0d342;'>{self.history.stars_show(stars)}</span></p></body></html>")
        self.card_maker.front = word
        self.card_maker.back = b_card
        self.card_maker.tag = tag
        self.card_maker.stars = self.history.stars_show(stars)
        if language == "EN":
            self.card_maker.deck = [language, self.settings_list[0][3]]
        elif language == "JP":
            self.card_maker.deck = [language, self.settings_list[0][1]]

        if language == "EN":
                
            if word != self.card_maker.last_word:
                self.history.set_history(word, stars, "EN")
                self.card_maker.last_word = word

            self.history.history_position_en[0] = self.history.get_rows("EN", self.sort_box.currentText(), self.filter_box.currentText())
            self.prev_button.setEnabled(False)
            if(self.history.get_rows("EN", self.sort_box.currentText(), self.filter_box.currentText()) <= 50):
                self.next_button.setEnabled(False)                
            self.history_en.setText(
            self.history.history_show(
            self.history.get_rows("EN", self.sort_box.currentText(), self.filter_box.currentText()), 
            self.sort_box.currentText(), 
            self.filter_box.currentText()))
            self.save_card.setEnabled(True)


    def gui_clean(self):

        self.save_card.setEnabled(True)
        self.front_card.setText(
        self.card_maker.front)
        self.back_card.setText(
        f"<center><br/><h2>{self.stars}<h2></center>{self.card_maker.back}")
        self.tag_card.setText(
        self.card_maker.tag)
        self.strs.setText(f"<html><head/><body><p><span style=' color:#f0d342;'>{self.card_maker.stars}</span></p></body></html>")


    def closeEvent(self, event):
        event.accept()


    def focusOutEvent(self, event):
        self.setWindowState(
        window.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.activateWindow()
        self.raise_()

    
    def history_settings_get(self):        
        
        self.history_en.setText(
        self.history.history_show(
        self.history.get_rows("EN", self.sort_box.currentText(), self.filter_box.currentText()), 
        self.sort_box.currentText(), 
        self.filter_box.currentText()))
        
        self.history.history_position_en[0] = self.history.get_rows("EN", self.sort_box.currentText(), self.filter_box.currentText())
        self.prev_button.setEnabled(False)
        if(self.history.get_rows("EN", self.sort_box.currentText(), self.filter_box.currentText()) <= 50):
            self.next_button.setEnabled(False)
        else:
            self.next_button.setEnabled(True)


    def history_prev(self):
         
        self.history.history_position_en[0] = self.history.history_position_en[0] + 50

        if(self.history.history_position_en[0] >= self.history.get_rows("EN", self.sort_box.currentText(), self.filter_box.currentText())):
            self.history.history_position_en[0] = self.history.get_rows("EN", self.sort_box.currentText(), self.filter_box.currentText())
            self.prev_button.setEnabled(False)

        if self.history.history_position_en[0] - 50 >= 0:
            self.next_button.setEnabled(True)
        else:
            self.next_button.setEnabled(False)

        self.history_en.setText(
        self.history.history_show(
        self.history.history_position_en[0], 
        self.sort_box.currentText(), 
        self.filter_box.currentText()))


    def history_next(self):

        self.history.history_position_en[0] = self.history.history_position_en[0] - 50

        if self.history.history_position_en[0] <= 50:
            self.next_button.setEnabled(False)

        if self.history.history_position_en[0] <= 0:
            self.history.history_position_en[0] = 0

        if self.history.history_position_en[0] + 50 >= self.history.get_rows("EN", self.sort_box.currentText(), self.filter_box.currentText()):
            self.prev_button.setEnabled(True)
        else:
            self.prev_button.setEnabled(True)

        self.history_en.setText(
        self.history.history_show(
        self.history.history_position_en[0], 
        self.sort_box.currentText(), 
        self.filter_box.currentText()))


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

window = MainWindow()
app.exec_()