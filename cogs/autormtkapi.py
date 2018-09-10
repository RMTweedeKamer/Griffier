import discord
from discord.ext import commands


class AutoRMTKAPI:
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils

        if 'AutoRMTKAPI' not in self.utils.settings:
            self.utils.settings['AutoRMTKAPI'] = {}
        if 'token' not in self.utils.settings['AutoRMTKAPI']:
            self.utils.settings['AutoRMTKAPI']['token'] = None
        if 'roles' not in self.utils.settings['AutoRMTKAPI']:
            self.utils.settings['AutoRMTKAPI']['roles'] = []

        self.utils.save_settings()

        self.autormtkapi_token = self.utils.settings['AutoRMTKAPI']['token']
        self.autormtk_roles = self.utils.settings['AutoRMTKAPI']['roles']

    @commands.group(name='autormtk')
    @commands.is_owner()
    async def autormtk(self, context):
        '''API instellingen voor AutoRMTK'''

    @autormtk.command(name='token')
    async def autormtk_set_token(self, context, token: str):
        '''Stel de token in'''
        self.utils.settings['AutoRMTKAPI']['token'] = token
        self.autormtkapi_token = self.utils.settings['AutoRMTKAPI']['token']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    @autormtk.command(name='rol')
    async def autormtk_add_role(self, context, rol: discord.Role):
        '''Voeg een rol toe die AutoRMTK mag bedienen'''
        roles = self.utils.settings['AutoRMTKAPI']['roles']
        if rol.id not in roles:

            roles.append(rol.id)

            self.utils.settings['AutoRMTKAPI']['roles'] = roles

            self.autormtk_roles = self.utils.settings['AutoRMTKAPI']['roles']
            self.utils.save_settings()

            await context.message.add_reaction('\U0001F44D')

        else:
            await context.send('\'{}\' heeft al bevoegdheden gekregen!'.format(rol.name))
