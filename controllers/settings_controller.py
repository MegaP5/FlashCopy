from models.settings import Settings

class SettingsController:
    def __init__(self):

        self.settings = Settings()

        self.settings.create_settings_table()
        self.settings.create_user() 

    def get_settings(self):
        return self.settings.get_settings()

    def set_settings(self, dict_jp, cm_jp, dict_en, cm_en, theme):
        self.settings.set_settings(dict_jp, cm_jp, dict_en, cm_en, theme)
