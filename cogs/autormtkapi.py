import discord
from discord.ext import commands
import aiohttp
import json


class AutoRMTKAPI:
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils

        if 'AutoRMTKAPI' not in self.utils.settings:
            self.utils.settings['AutoRMTKAPI'] = {}
        if 'token' not in self.utils.settings['AutoRMTKAPI']:
            self.utils.settings['AutoRMTKAPI']['token'] = None

        self.utils.save_settings()

        self.autormtkapi_token = self.utils.settings['AutoRMTKAPI']['token']
        self.autormtk_roles = self.utils.settings['AutoRMTKAPI']['roles']

        self.autormtk_gateway = 'http://rmtk.ngrok.io/{}'

    async def get_request(self, member, resource_type):
        if self.autormtkapi_token:
            headers = {'Authorization': 'Bearer {}:{}'.format(self.autormtkapi_token, str(member.id)),
                       'Content-Type': 'application/vnd.api+json'
                       }

            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(self.autormtk_gateway.format(resource_type)) as response:
                    data = await response.read()
                    data = json.loads(data)
                await session.close()
                return data
        else:
            return 'No token set!'

    async def post_request(self, member, resource_type, payload):
        if self.autormtkapi_token:
            headers = {'Authorization': 'Bearer {}:{}'.format(self.autormtkapi_token, str(member.id))}
            data_type = {'Content-Type': 'application/vnd.api+json',
                         'Accept': 'application/vnd.api+json'}

            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(self.autormtk_gateway.format(resource_type),
                                        json=payload,
                                        headers=data_type) as response:
                    data = await response.read()
                    data = json.loads(data)
                await session.close()
                return data
        else:
            return 'No token set!'

    @commands.command(name='tr')
    async def testrequest(self, context):

        # {
        #  'id': '1',
        #  'type': 'users',
        #  'links': {
        #            'self': 'http://rmtk.ngrok.io/users/1'
        #           },
        #  'attributes': {
        #                 'username': 'Dali'
        #                 'discord-id': None
        #                }
        # }

        payload = {
                      "data": {
                        "type": "users",
                        "attributes": {
                          "username": "Ember Hamster",
                          "discord-id": str(context.author.id)
                        }
                      }
                }
        results = await self.post_request(context.author, 'users', payload=payload)
        print(results)

        results = await self.get_request(context.author, 'profile')
        print(results)

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
