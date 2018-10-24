import discord
from discord.ext import commands


class Groeter:
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils

        if 'groeter' not in self.utils.settings:
            self.utils.settings['groeter'] = {}
        if 'kanaal' not in self.utils.settings['groeter']:
            self.utils.settings['groeter']['kanaal'] = None
        if 'bericht' not in self.utils.settings['groeter']:
            self.utils.settings['groeter']['bericht'] = None

        self.utils.save_settings()

        self.groet_kanaal = self.utils.settings['groeter']['kanaal']
        self.groet_bericht = self.utils.settings['groeter']['bericht']

    @commands.group(name='groeter')
    @commands.is_owner()
    async def groeter(self, context):
        '''Instellingen voor de groeter'''
        if not context.invoked_subcommand:
            await self.utils.send_cmd_help(context)

    @groeter.command(name='kanaal')
    async def groeter_set_kanaal(self, context, kanaal: discord.TextChannel):
        '''Stel een kanaal in waar nieuwe gebruikers begroet moeten worden.'''
        self.utils.settings['groeter']['kanaal'] = kanaal.id
        self.groet_kanaal = self.utils.settings['groeter']['kanaal']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    @groeter.command(name='bericht')
    async def groeter_set_bericht(self, context, *, bericht: str):
        '''Stel een bericht in waarmee de nieuwe gebruikers begroet moeten worden.'''
        self.utils.settings['groeter']['bericht'] = ''.join(bericht)
        self.groet_bericht = self.utils.settings['groeter']['bericht']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    async def on_member_join(self, member):
        if self.groet_kanaal and self.groet_bericht:
            kanaal = self.bot.get_channel(self.groet_kanaal)
            await kanaal.send(self.groet_bericht.format(member=member))
