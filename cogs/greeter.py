import discord
from discord.ext import commands


class Greeter(commands.Cog):
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils

        if 'greeter' not in self.utils.settings:
            self.utils.settings['greeter'] = {}
        if 'channel' not in self.utils.settings['greeter']:
            self.utils.settings['greeter']['channel'] = None
        if 'message' not in self.utils.settings['greeter']:
            self.utils.settings['greeter']['message'] = None

        self.utils.save_settings()

        self.greet_channel = self.utils.settings['greeter']['channel']
        self.greet_message = self.utils.settings['greeter']['message']

    @commands.group(name='greeter')
    @commands.has_any_role(488363614294507541, 488361925575573505)
    async def greeter(self, context):
        '''Instellingen voor de groeter'''
        if not context.invoked_subcommand:
            await self.utils.send_cmd_help(context)

    @greeter.command(name='channel', aliases=['kanaal'])
    async def set_greeter_channel(self, context, channel: discord.TextChannel):
        '''Stel een kanaal in waar nieuwe gebruikers begroet moeten worden.'''
        self.utils.settings['greeter']['channel'] = channel.id
        self.greet_channel = self.utils.settings['greeter']['channel']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    @greeter.command(name='message', aliases=['bericht'])
    async def set_greeter_message(self, context, *, message: str):
        '''Stel een bericht in waarmee de nieuwe gebruikers begroet moeten worden.'''
        self.utils.settings['greeter']['message'] = ''.join(message)
        self.greet_message = self.utils.settings['greeter']['message']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.greet_channel and self.greet_message:
            channel = self.bot.get_channel(self.greet_channel)
            await channel.send(self.greet_message.format(member=member))
