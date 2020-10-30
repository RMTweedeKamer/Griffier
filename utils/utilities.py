import json
from discord.ext import commands


class Utils:
    def __init__(self, bot,):
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

    def jail_check(self, command, channel):
        command = command.name
        if command in self.settings['jail']:
            if channel in self.settings['jail'][command]:
                return False
        return True

    async def send_cmd_help(self, context):
        if context.invoked_subcommand:
            await context.send_help(context.invoked_subcommand)
        else:
            await context.send_help(context.command)

    async def chunks(self, l, n):
        # For item i in a range that is a length of l,
        x = []
        for i in range(0, len(l), n):
            # Create an index range for l of n items:
            x.append(l[i:i+n])
        return x
