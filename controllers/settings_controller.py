from models.settings import Settings

class SettingsController:
    def __init__(self):

        self.settings = Settings()

        self.settings.create_settings_table()
        self.settings.create_hotkeys_table()
        self.settings.create_user()
        self.settings.create_default_hotkeys()

    def get_settings(self):
        return self.settings.get_settings()


    def get_hotkeys_list(self):
        return self.settings.get_hotkeys()


    def set_settings(
    self, dict_jp, cm_jp, dict_en, cm_en, 
    theme, fill_key_a, fill_key_b, front_key_a, 
    front_key_b, back_key_a, back_key_b, tag_key_a, 
    tag_key_b):
        self.settings.set_settings(dict_jp, cm_jp, dict_en, cm_en, 
        theme, fill_key_a, fill_key_b, front_key_a, 
        front_key_b, back_key_a, back_key_b, tag_key_a, 
        tag_key_b)