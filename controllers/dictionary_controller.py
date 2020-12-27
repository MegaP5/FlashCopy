import os

from models.dictionary import Dictionary
from models.settings import Settings

class DictionaryController:
    def __init__(self):

        self.dictionary = Dictionary()
        self.settings = Settings()


    def get_dict_list_jp(self):

        dict_list = []
        dict_folders = next(os.walk('./app_data/dictionary/JP/'))[1]

        for dict_folder in dict_folders:
            if os.path.exists("./app_data/dictionary/JP/" + dict_folder + "/main.py"):
                dict_list.append(dict_folder)

        return dict_list


    def get_dict_list_en(self):

        dict_list = []
        dict_folders = next(os.walk('./app_data/dictionary/EN/'))[1]

        for dict_folder in dict_folders:
            if os.path.exists("./app_data/dictionary/EN/" + dict_folder + "/main.py"):
                dict_list.append(dict_folder)

        return dict_list


    def get_dict_url(self, language, word):

        if language == "JP":
            name = self.settings.get_settings()[0][0]
        elif language == "EN":
            name = self.settings.get_settings()[0][2]
        else:
            return "https://translate.google.com.br/?hl=pt-BR&tab=wT#view=home&op=translate&sl=auto&tl=en&text=" + word
        return self.dictionary.get_url(name, language).replace("{word}", word)
