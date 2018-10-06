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

    async def send_cmd_help(self, context):
        if context.invoked_subcommand:
            pages = await self.bot.formatter.format_help_for(context, context.invoked_subcommand)
            for page in pages:
                await context.send(page)
        else:
            pages = await self.bot.formatter.format_help_for(context, context.command)
            for page in pages:
                await context.send(page)
