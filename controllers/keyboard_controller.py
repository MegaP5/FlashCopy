import pyautogui as pya
import pyperclip
import time
from pynput import keyboard

from PyQt5.QtCore import Qt, QThread, pyqtSignal

from controllers.clipboard_controller import ClipboardController
from controllers.history_controller import HistoryController



class KeyboardController(QThread):
    
    tag_value = pyqtSignal(str)
    back_value = pyqtSignal(str)
    front_value = pyqtSignal(str)
    auto_fill = pyqtSignal(str, str, str, int, str)


    def __init__(self, parent=None):
        super().__init__(parent)
        self.clipboard = ClipboardController()
        self.history = HistoryController()


    def function_1(self):
        print('Function 1 activated')

    def function_2(self):
        print('Function 2 activated')


    def run(self):

        with keyboard.GlobalHotKeys({
                '<ctrl>+1': self.auto_fill_function,
                '<ctrl>+2': self.front_function,
                '<ctrl>+3': self.back_function,
                '<ctrl>+4': self.tag_function}) as h:
            h.join()


    def copy_selected_text(self):
        pya.hotkey('ctrl', 'c')
        time.sleep(.01)
        return pyperclip.paste()


    def auto_fill_function(self):

        cp = self.copy_selected_text()

        gui_data = self.clipboard.clipboard_check(cp)

        self.auto_fill.emit(gui_data[0], gui_data[1], gui_data[2], gui_data[3], gui_data[4])    
        #self.front_value.emit(gui_data[0])
        #self.back_value.emit(f"<center><br/><h2>{self.history.stars_show(gui_data[3])}<h2></center>{gui_data[1]}")
        #self.tag_value.emit(gui_data[2])    


    def front_function(self):
        cp = self.copy_selected_text()
        self.front_value.emit(cp)


    def back_function(self):        
        self.back_value.emit("back!")
        

    def tag_function(self):
        self.tag_value.emit("works!")