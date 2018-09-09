import discord
import asyncio
from discord.ext import commands
import aiohttp

from utils.error_handler import CommandErrorHandler
from utils.utilities import Utils
from cogs.private_channels import PrivateChannels

token = ''
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
        await context.message.add_reaction('\U0001F3D3')

    @commands.command(name='shutdown')
    @commands.is_owner()
    async def shutdown_bot(self, context):
        await context.message.add_reaction('\U0001F44D')
        await bot.logout()

    @commands.group(name='update')
    @commands.is_owner()
    async def update(self, context):
        pass

    @update.command(name='avatar')
    async def avatar(self, context, url: str):
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

    @update.command(name='username')
    async def _username(self, context, *, username: str):
        try:
            await self._name(name=username)
        except discord.HTTPException:
            await context.send('Failed to change name. Remember that you can '
                               'only do it up to 2 times an hour.'
                               )
        else:
            await context.send('Done.')


bot = commands.Bot(command_prefix=prefix, activity=discord.Activity(name='NPO Polertiek', type=discord.ActivityType.watching))

# Data manager and stuff...
utils = Utils(bot)

# Utils
bot.add_cog(Griffier(bot))
bot.add_cog(CommandErrorHandler(bot))

# Cogs
bot.add_cog(PrivateChannels(bot, utils))

bot.run(token)
