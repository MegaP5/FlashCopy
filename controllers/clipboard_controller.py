import re
import importlib
import unicodedata

import app_data.verb_maker.japanese.main as desc
import app_data.frequency.frequency as frequency

from controllers.card_maker_controller import CardMakerController
from controllers.settings_controller import SettingsController

class ClipboardController:
    def __init__(self):
        self.settings = SettingsController()


        self.settings_list = self.settings.get_settings()

        # LOAD THE DEFAULT DICTIONARY
        try:
            self.jp_dict = importlib.import_module("app_data.dictionary.JP." + self.settings_list[0][1] + ".main")
            self.en_dict = importlib.import_module("app_data.dictionary.EN." + self.settings_list[0][3] + ".main")
        except ModuleNotFoundError:
            print("Dictionary not found")


    def clipboard_check(self, clipboard):   


        if type(clipboard) == str:  
        
            clipboard = clipboard.strip()
            edited_clipboard = self.clipboard_edit(clipboard)

            if " " in clipboard:

                return clipboard, "", "", "", "None"

            elif unicodedata.category(edited_clipboard[0]) == "Lo":     

                word_desc = desc.r_conj(edited_clipboard)
                definitions = self.jp_dict.main(word_desc)
                stars = frequency.f_stars("JP", word_desc)

                b_card = ""

                try:
                    for wo in definitions:
                        b_card = b_card + f"<center>{wo[5][0]}</center>"

                except:
                    print(f"{word_desc} not found in dictionary")

                return word_desc, b_card, word_desc, stars, "JP"

            else:

                stars = frequency.f_stars("EN", edited_clipboard)
                ba_card = self.en_dict.main(edited_clipboard)

                b_card = []
                for b in ba_card:              
                    b_card.append(b.replace('\n', ''))

                return edited_clipboard, b_card[0], edited_clipboard, stars, "EN"



    def clipboard_edit(self, word):

        word = word.lower()
        word = word.replace('\n', '')
        word_re = re.sub('[!,*)@#%(&$_?.^]', '', word)

        if word_re != "":
            word = word_re

        return word