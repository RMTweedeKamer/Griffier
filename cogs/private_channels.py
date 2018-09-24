import discord
from discord.ext import commands


class PrivateChannels:
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils

        if 'private_channels' not in self.utils.settings:
            self.utils.settings['private_channels'] = {}
        if 'category' not in self.utils.settings['private_channels']:
            self.utils.settings['private_channels']['category'] = None

        self.utils.save_settings()

        self.offtopic_category = self.utils.settings['private_channels']['category']

    @commands.group(name='privatekanaal', aliases=['pk', 'privatechannel', 'pc'])
    async def privatechannel(self, context):
        '''Maak je eigen private kanelen aan'''

    @privatechannel.command(name='categorie', aliases=['category'])
    @commands.is_owner()
    async def privatechannel_set_category(self, context, categorie: discord.CategoryChannel):
        '''Kies welke categorie je wilt gebruiken'''
        self.utils.settings['private_channels']['category'] = categorie.id
        self.offtopic_category = self.utils.settings['private_channels']['category']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    @privatechannel.command(name='open', aliases=['new'])
    async def privatechannel_new_channel(self, context, *, channel_name: str):
        '''Open een nieuw private kanaal'''
        if self.offtopic_category:
            guild = context.guild
            channel_name = channel_name.replace(' ', '-')

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                context.author: discord.PermissionOverwrite(read_messages=True)
            }

            category = discord.utils.get(guild.categories,
                                         id=self.offtopic_category)

            await guild.create_text_channel(channel_name,
                                            category=category,
                                            overwrites=overwrites)
            await context.message.add_reaction('\U0001F44D')

    @privatechannel.command(name='verzoek', aliases=['invite'])
    async def privatechannel_invite_to_channel(self, context, member: discord.Member):
        '''Nodig iemand uit om een private kanaal te betreden'''
        await context.channel.set_permissions(member,
                                              read_messages=True)
        await context.message.add_reaction('\U0001F44D')

    # Kleuters...
    # @privatechannel.command(name='schop', aliases=['kick'])
    # async def privatechannel_kick_from_channel(self, context, member: discord.Member):
    #    '''Schop iemand uit het private kanaal'''
    #    await context.channel.set_permissions(member,
    #                                          read_messages=False)
    #    await context.message.add_reaction('\U0001F44D')

    @privatechannel.command(name='verlaat', aliases=['leave'])
    async def privatechannel_leave_from_channel(self, context):
        '''Verlaat een private kanaal'''
        member = context.author
        await context.channel.set_permissions(member,
                                              read_messages=False)
        await context.message.add_reaction('\U0001F44D')
