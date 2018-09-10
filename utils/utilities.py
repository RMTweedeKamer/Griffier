import json


class Utils:
    def __init__(self, bot):
        self.bot = bot
        self.settings_file = 'data/settings.json'

        self.settings = self.load_json(self.settings_file)

    def save_json(self, filename, data):
        with open(filename, encoding='utf-8', mode="w") as f:
            json.dump(data, f, indent=4, sort_keys=True, separators=(',', ' : '))
        return data

    def load_json(self, filename):
        with open(filename, encoding='utf-8', mode="r") as f:
            data = json.load(f)
        return data

    def save_settings(self):
        self.save_json(self.settings_file, self.settings)
