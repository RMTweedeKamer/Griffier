import discord
from discord.ext import commands


class Mute(commands.Cog):
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils

    @commands.command(name='mute', aliases=['zwijg'])
    @commands.has_any_role('Secretaris-Generaal', 'Voorzitter', 'Ondervoorzitter')
    async def mute(self, context, member: discord.Member):
        '''Leg iemand het zwijgen op.'''
        await context.channel.set_permissions(member, send_messages=False)
        await context.message.add_reaction('\U0001F44B')

    @commands.command(name='unmute', aliases=['spreek'])
    @commands.has_any_role('Secretaris-Generaal', 'Voorzitter', 'Ondervoorzitter')
    async def unmute(self, context, member: discord.Member):
        '''Iemand mag weer spreken'''
        await context.channel.set_permissions(member, send_messages=True)
        await context.message.add_reaction('\U0001F44D')
