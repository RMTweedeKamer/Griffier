# Defaults
import json
import os

# Discord
import discord
from discord.ext import commands

# Derde partij
import aiohttp

# Laad alle cogs
from utils.error_handler import CommandErrorHandler
from utils.utilities import Utils
from cogs.customchannels import CustomChannels
# from cogs.autormtkapi import AutoRMTKAPI
from cogs.announcements import Announcements
from cogs.greeter import Greeter
from cogs.starboard import Starboard
from cogs.pinner import Pinner
from cogs.eightball import Eightball
from cogs.zoltar import Zoltar
from cogs.mute import Mute


class Griffier():
    def __init__(self, bot, host_id, utils):
        self.bot = bot
        self.host_id = host_id
        self.utils = utils

    async def on_command_error(self, context, error):
        if isinstance(error, commands.UserInputError):
            await context.send('```{}```'.format(error))
            await self.utils.send_cmd_help(context)

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
    async def shutdown_bot(self, context):
        '''Sluit Griffier af'''
        if context.author.id == self.host_id:
            await context.send('Deze zitting is gesloten.')
            await bot.logout()

    @commands.command(name='devupdate')
    async def dev(self, context):
        '''Update the bot to the dev branch'''
        if 'Developer' in [role.name for role in context.author.roles]:
            message = await context.send('Updating...')
            os.chdir('../')
            os.system('mkdir temp')
            os.system('cp development/data/settings.json temp')
            os.system('cp development/config.json temp')
            os.system('rm -rf development')
            os.system('git clone -b dev --single-branch https://github.com/RMTweedeKamer/Griffier.git development')
            os.system('mkdir development/data')
            os.system('cp temp/settings.json development/data')
            os.system('cp temp/config.json development')
            os.chdir('development')
            await message.edit(content='Restarting...')
            await bot.logout()
        else:
            await context.send('You don\'t have the correct permissions to do this.')

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


if not os.path.exists('data/settings.json'):
    with open('data/settings.json', encoding='utf-8', mode='w') as f:
        f.write(json.dumps({}))
        f.close()

if not os.path.exists('config.json'):
    with open('config.json', encoding='utf-8', mode='w') as f:
        token = input('token> ')
        host_id = input('member id of hoster> ')
        prefix = input('prefix> ')
        config = json.dumps({'token': token, 'host_id': host_id, 'prefix': prefix})
        f.write(config)
        f.close()

with open('config.json', encoding='utf-8', mode='r') as f:
        config = json.load(f)

token = config['token']
host_id = config['host_id']
prefix = config['prefix']

bot = commands.Bot(command_prefix=prefix,
                   activity=discord.Activity(name='NPO Polertiek',
                                             type=discord.ActivityType.watching))

# Data manager en zo...
utils = Utils(bot)

# De bot
bot.add_cog(Griffier(bot, host_id, utils))
bot.add_cog(CommandErrorHandler(bot))

# Laad cogs
bot.add_cog(CustomChannels(bot, utils))
# bot.add_cog(AutoRMTKAPI(bot, utils))
bot.add_cog(Announcements(bot, utils))
bot.add_cog(Greeter(bot, utils))
bot.add_cog(Starboard(bot, utils))
bot.add_cog(Pinner(bot, utils))
bot.add_cog(Eightball(bot, utils))
bot.add_cog(Zoltar(bot, utils))
bot.add_cog(Mute(bot, utils))
try:
    bot.run(token)
except Exception as e:
    print(e)
finally:
    exit(26)
