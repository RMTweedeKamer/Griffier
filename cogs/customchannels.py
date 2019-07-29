import discord
from discord.ext import commands
from datetime import datetime, timedelta


# TODO

class CustomChannels():
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils

        if 'custom_channels' not in self.utils.settings:
            self.utils.settings['custom_channels'] = {}
        if 'category' not in self.utils.settings['custom_channels']:
            self.utils.settings['custom_channels']['category'] = None
        if 'private_category' not in self.utils.settings['custom_channels']:
            self.utils.settings['custom_channels']['private_category'] = None
        if 'public_channels' not in self.utils.settings['custom_channels']:
            self.utils.settings['custom_channels']['public_channels'] = []
        if 'private_channels' not in self.utils.settings['custom_channels']:
            self.utils.settings['custom_channels']['private_channels'] = []
        if 'invite_message' not in self.utils.settings['custom_channels']:
            self.utils.settings['custom_channels']['invite_message'] = "{member.mention}, is toegevoegd aan dit kanaal!"

        self.utils.save_settings()

        self.offtopic_category = self.utils.settings['custom_channels']['category']
        self.private_category = self.utils.settings['custom_channels']['private_category']
        self.public_channels = self.utils.settings['custom_channels']['public_channels']
        self.private_channels = self.utils.settings['custom_channels']['private_channels']
        self.invite_message = self.utils.settings['custom_channels']['invite_message']
        self.description_message = "De beschrijving van dit kanaal is aangepast."
        self.purge_message = "Alle oude kanalen zijn verwijderd."
        self.create_message = " is aangemaakt!"

    async def on_guild_channel_delete(self, channel):
        if channel.id in self.public_channels:
            public_channels = self.utils.settings['custom_channels']['public_channels']
            public_channels.remove(channel.id)

            self.utils.settings['custom_channels']['public_channels'] = public_channels
            self.public_channels = self.utils.settings['custom_channels']['public_channels']
            self.utils.save_settings()
        elif channel.id in self.private_channels:
            private_channels = self.utils.settings['custom_channels']['private_channels']
            private_channels.remove(channel.id)

            self.utils.settings['custom_channels']['private_channels'] = private_channels
            self.private_channels = self.utils.settings['custom_channels']['private_channels']
            self.utils.save_settings()

    @commands.group(name='customchannel', aliases=['cc'])
    async def customchannel(self, context):
        '''Laat gebruikers hun eigen kanalen aanmaken'''
        if not context.invoked_subcommand:
            await self.utils.send_cmd_help(context)

    @customchannel.command(name='list', aliases=['lijst'])
    async def customchannel_list_directory(self, context):
        '''Laat alle publieke kanalen zien'''

        channels = '\n\n'
        for channel in self.public_channels:
            ch = self.bot.get_channel(channel)
            channels += '{} ({})\n'.format(ch.mention, ch.id)
        embed = discord.Embed(color=discord.Color.red(), description=channels, title='Alle publieke kanalen')
        await context.send(embed=embed)
        # await context.message.add_reaction('\U0001F44D')

    @customchannel.command(name='join', aliases=['betreed'])
    async def customchannel_join_channel(self, context, channel: discord.TextChannel):
        '''Betreed een publiek kanaal'''
        if channel.id in self.public_channels:
            channel = self.bot.get_channel(channel.id)
            member = context.author
            await channel.set_permissions(member,
                                          read_messages=True)
            await context.message.delete()

    @customchannel.command(name='description', aliases=['beschrijving'])
    async def customchannel_change_description_channel(self, context, *, description: str):
        '''Verander beschrijving van een kanaal'''
        channel = context.channel
        description = ''.join(description)
        if channel.id in self.public_channels or channel.id in self.private_channels:
            channel = self.bot.get_channel(channel.id)
            await channel.edit(topic=description)
            await context.channel.send(self.description_message)
            await context.message.delete()

    @customchannel.command(name='category')
    @commands.is_owner()
    async def customchannel_set_category(self, context, categorie: discord.CategoryChannel):
        '''Kies welke categorie je wilt gebruiken om alle kanalen in kwijt te kunnen'''
        self.utils.settings['custom_channels']['category'] = categorie.id
        self.offtopic_category = self.utils.settings['custom_channels']['category']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    @customchannel.command(name='private_category')
    @commands.is_owner()
    async def customchannel_set_private_category(self, context, categorie: discord.CategoryChannel):
        '''Kies welke categorie je wilt gebruiken om prive kanalen in kwijt te kunnen'''
        self.utils.settings['custom_channels']['private_category'] = categorie.id
        self.offtopic_category = self.utils.settings['custom_channels']['private_category']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    @customchannel.command(name='private', aliases=['prive'])
    async def customchannel_new_channel(self, context, *, channel_name: str):
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
                                         id=self.private_category)

            channel = await guild.create_text_channel(channel_name,
                                                      category=category,
                                                      overwrites=overwrites)

            private_channels = self.utils.settings['custom_channels']['private_channels']
            private_channels.append(channel.id)

            self.utils.settings['custom_channels']['private_channels'] = private_channels
            self.private_channels = self.utils.settings['custom_channels']['private_channels']
            self.utils.save_settings()

            await context.channel.send("Privékanaal" + self.create_message)
            await context.message.delete()

    @customchannel.command(name='public', aliases=['publiek'])
    async def customchannel_new_public_channel(self, context, *, channel_name: str):
        '''Open een nieuw publiek kanaal'''
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

            channel = await guild.create_text_channel(channel_name,
                                                      category=category,
                                                      overwrites=overwrites)

            public_channels = self.utils.settings['custom_channels']['public_channels']
            public_channels.append(channel.id)

            self.utils.settings['custom_channels']['public_channels'] = public_channels
            self.public_channels = self.utils.settings['custom_channels']['public_channels']
            self.utils.save_settings()

            await context.channel.send("Kanaal " + channel_name + self.create_message)
            await context.message.delete()

    @customchannel.command(name='invite', aliases=['verzoek'])
    async def customchannel_invite_to_channel(self, context, member: discord.Member):
        '''Nodig iemand uit om een private kanaal te betreden'''
        await context.channel.set_permissions(member,
                                              read_messages=True)
        await context.channel.send(self.invite_message.format(member=member))
        await context.message.delete()

    @customchannel.command(name='set_invite')
    @commands.is_owner()
    async def customchannel_set_invite_message(self, context, *, message: str):
        '''Stel een bericht in waarmee de uitgenodigde mensen begroet moeten worden.'''
        self.utils.settings['custom_channels']['invite_message'] = ''.join(message)
        self.invite_message = self.utils.settings['custom_channels']['invite_message']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    @customchannel.command(name='purge_check')
    @commands.is_owner()
    async def customchannel_check_purge_old_channels(self, context, term: int):
        '''Controleer alle kanalen of ze inactief zijn sinds dan de meegegeven waarde'''
        channels = '\n\n'
        for channel in self.public_channels:
            ch = self.bot.get_channel(channel)
            last_message = await ch.history(limit=1).next()
            timelimit = datetime.now() - timedelta(days=term)
            if last_message.created_at < timelimit:
                channels += '{} ({})\n'.format(ch.mention, ch.id)
        embed = discord.Embed(color=discord.Color.red(), description=channels, title='Kanalen die verwijderd zouden worden')
        await context.send(embed=embed)

    @customchannel.command(name='purge_for_real')
    @commands.is_owner()
    async def customchannel_purge_old_channels(self, context, term: int):
        '''Verwijder alle kanalen die inactief zijn sinds de meegegeven waarde'''
        for channel in self.public_channels:
            ch = self.bot.get_channel(channel)
            last_message = await ch.history(limit=1).next()
            timelimit = datetime.now() - timedelta(days=term)
            if last_message.created_at < timelimit:
                await ch.delete()
        await context.channel.send(self.purge_message)
        await context.message.delete()


    # Kleuters...
    # @privatechannel.command(name='schop', aliases=['kick'])
    # async def privatechannel_kick_from_channel(self, context, member: discord.Member):
    #    '''Schop iemand uit het private kanaal'''
    #    await context.channel.set_permissions(member,
    #                                          read_messages=False)
    #    await context.message.add_reaction('\U0001F44D')

    @customchannel.command(name='leave', aliases=['verlaat'])
    async def customchannel_leave_from_channel(self, context):
        '''Verlaat een private kanaal'''
        member = context.author
        await context.channel.set_permissions(member,
                                              read_messages=False)
        await context.message.delete()