# Discord
import discord
from discord.ext import commands

# Derde partij
import aiohttp

# Laad alle cogs
from utils.error_handler import CommandErrorHandler
from utils.utilities import Utils
from cogs.private_channels import PrivateChannels
from cogs.autormtkapi import AutoRMTKAPI

token = 'NDg4NDAxNTUyNjcxNzY4NTc3.Dnbskw.HWrVe7Wy_ZaOrBBHCQQlapZODb8'
prefix = '//'


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
        await context.message.add_reaction('\U0001F44D')
        await bot.logout()

    @commands.group(name='update')
    @commands.is_owner()
    async def update(self, context):
        '''Werk de bot bij'''

    @update.command(name='afbeelding', aliases=['avatar'])
    async def avatar(self, context, url: str):
        '''Verander de afbeelding van Griffier'''
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                data = await r.read()

        try:
            await context.bot.user.edit(avatar=data)
        except discord.HTTPException:
            await context.send('Failed. Remember that you can edit my avatar '
                               'up to two times a hour. The URL must be a '
                               'direct link to a JPG / PNG.')
        except discord.InvalidArgument:
            await context.send('JPG / PNG format only.')
        else:
            await context.message.add_reaction('\U0001F44D')

    @update.command(name='gebruikersnaam', aliases=['username'])
    async def _username(self, context, *, username: str):
        '''Verander de gebruikersnaam van Griffier'''
        try:
            await self._name(name=username)
        except discord.HTTPException:
            await context.send('Failed to change name. Remember that you can '
                               'only do it up to 2 times an hour.')
        else:
            await context.message.add_reaction('\U0001F44D')


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
bot.add_cog(AutoRMTKAPI(bot, utils))

bot.run(token)
