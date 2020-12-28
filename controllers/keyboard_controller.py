import pyautogui as pya
import pyperclip
import time
from pynput import keyboard

from PyQt5.QtCore import Qt, QThread, pyqtSignal

from controllers.clipboard_controller import ClipboardController
from controllers.history_controller import HistoryController

from models.settings import Settings

class KeyboardController(QThread):
    
    tag_value = pyqtSignal(str)
    back_value = pyqtSignal(str)
    front_value = pyqtSignal(str)
    auto_fill = pyqtSignal(str, str, str, int, str)    


    def __init__(self, parent=None):
        super().__init__(parent)
        self.clipboard = ClipboardController()
        self.history = HistoryController()

        self.settings = Settings()

        # get hotkeys from DB and save in a tuple.
        self.hotkeys = self.get_hotkeys_list()


    def get_hotkeys_list(self):
        return self.settings.get_hotkeys()


    def run(self):

        with keyboard.GlobalHotKeys({
                self.hotkeys[0][0]: self.auto_fill_function,
                self.hotkeys[0][1]: self.front_function,
                self.hotkeys[0][2]: self.back_function,
                self.hotkeys[0][3]: self.tag_function}) as h:
            h.join()


    def copy_selected_text(self):
        pya.hotkey('ctrl', 'c')
        time.sleep(.01)
        return pyperclip.paste()


    def auto_fill_function(self):

        cp = self.copy_selected_text()

        gui_data = self.clipboard.clipboard_check(cp)

        self.auto_fill.emit(gui_data[0], gui_data[1], gui_data[2], gui_data[3], gui_data[4])


    def front_function(self):
        cp = self.copy_selected_text()
        self.front_value.emit(cp)


    def back_function(self):
        cp = self.copy_selected_text()
        self.back_value.emit(cp)
        

    def tag_function(self):
        cp = self.copy_selected_text()
        self.tag_value.emit(cp)