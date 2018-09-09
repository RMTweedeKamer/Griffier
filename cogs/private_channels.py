from discord.ext import commands
import discord


class PrivateChannels:
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils

        self.offtopic_category = 488363835217018881

    @commands.command(name='newchannel')
    async def create_new_channel(self, context, channel_name: str):
        guild = context.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            context.author: discord.PermissionOverwrite(read_messages=True)
        }

        category = discord.utils.get(context.guild.categories, id=self.offtopic_category)

        await guild.create_text_channel(channel_name,
                                        category=category,
                                        overwrites=overwrites)

        await context.message.add_reaction('\U0001F44D')

    @commands.command(name='invite')
    async def invite_to_channel(self, context, member: discord.Member):
        await context.channel.set_permissions(member,
                                              read_messages=True)
        await context.message.add_reaction('\U0001F44D')

    @commands.command(name='kick')
    async def kick_from_channel(self, context, member: discord.Member):
        await context.channel.set_permissions(member,
                                              read_messages=False)
        await context.message.add_reaction('\U0001F44D')

    @commands.command(name='leave')
    async def leave_from_channel(self, context):
        member = context.author
        await context.channel.set_permissions(member,
                                              read_messages=False)

        await context.message.add_reaction('\U0001F44D')
