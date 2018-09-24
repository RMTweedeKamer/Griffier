# Discord
import discord
from discord.ext import commands

# Derde partij
import aiohttp

# Laad alle cogs
from utils.error_handler import CommandErrorHandler
from utils.utilities import Utils
from cogs.private_channels import PrivateChannels
# from cogs.autormtkapi import AutoRMTKAPI
from cogs.aankondigingen import Aankondigingen
from cogs.groeter import Groeter


class Griffier():
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        print('Ingelogd als')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=0'.format(self.bot.user.id))
        print('-' * 20)

    @commands.command(name='ping')
    async def ping(self, context):
        '''Stuur een ping-pong balletje'''
        await context.message.add_reaction('\U0001F3D3')

    @commands.command(name='afsluiten', aliases=['shutdown'])
    @commands.is_owner()
    async def shutdown_bot(self, context):
        '''Sluit Griffier af'''
        await context.send('Deze zitting is gesloten.')
        await bot.logout()

    @commands.group(name='update')
    @commands.is_owner()
    async def update(self, context):
        '''De bot bijwerken'''

    @update.command(name='afbeelding', aliases=['avatar'])
    async def avatar(self, context, url: str):
        '''Verander de afbeelding van Griffier'''
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                data = await r.read()

        try:
            await context.bot.user.edit(avatar=data)
        except discord.HTTPException:
            await context.send('Het veranderen van de afbeelding is mislukt. Je kunt de afbeelding '
                               'slechts 2 keer per uur veranderen.')
        except discord.InvalidArgument:
            await context.send('Alleen JPG of PNG formaat.')
        else:
            await context.message.add_reaction('\U0001F44D')

    @update.command(name='gebruikersnaam', aliases=['username'])
    async def _username(self, context, *, username: str):
        '''Verander de gebruikersnaam van Griffier'''
        try:
            await self.bot.user.edit(name=username)
        except discord.HTTPException:
            await context.send('Kon de gebruikersnaam niet veranderen. Je kunt maar '
                               '2 keer per uur de gebruikersnaam veranderen.')
        else:
            await context.message.add_reaction('\U0001F44D')


token = 'NDg4NDAxNTUyNjcxNzY4NTc3.Dnbskw.HWrVe7Wy_ZaOrBBHCQQlapZODb8'
prefix = '//'

bot = commands.Bot(command_prefix=prefix,
                   activity=discord.Activity(name='NPO Polertiek',
                                             type=discord.ActivityType.watching))

# Data manager en zo...
utils = Utils(bot)

# De bot
bot.add_cog(Griffier(bot))
bot.add_cog(CommandErrorHandler(bot))

# Laad cogs
bot.add_cog(PrivateChannels(bot, utils))
# bot.add_cog(AutoRMTKAPI(bot, utils))
bot.add_cog(Aankondigingen(bot, utils))
bot.add_cog(Groeter(bot, utils))

bot.run(token)
