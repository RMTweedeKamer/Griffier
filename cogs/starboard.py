import discord
from discord.ext import commands
from datetime import datetime


class Starboard:
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils

        if 'starboard' not in self.utils.settings:
            self.utils.settings['starboard'] = {}
        if 'messages' not in self.utils.settings['starboard']:
            self.utils.settings['starboard']['messages'] = []
        if 'channel' not in self.utils.settings['starboard']:
            self.utils.settings['starboard']['channel'] = None
        if 'treshold' not in self.utils.settings['starboard']:
            self.utils.settings['starboard']['treshold'] = 3

        self.utils.save_settings()

        self.star_channel = self.utils.settings['starboard']['channel']
        self.threshold = self.utils.settings['starboard']['treshold']
        self.starred_messages = self.utils.settings['starboard']['messages']

        self.emoji = '⭐'

    @commands.group(name='starboard')
    @commands.is_owner()
    async def starboard(self, context):
        '''Instellingen voor pinner'''
        if not context.invoked_subcommand:
            await self.utils.send_cmd_help(context)

    @starboard.command(name='treshold')
    async def set_treshold(self, context, treshold: int):
        '''Treshold'''
        self.utils.settings['starboard']['treshold'] = treshold
        self.star_channel = self.utils.settings['starboard']['treshold']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    @starboard.command(name='channel')
    async def set_channel(self, context, channel: discord.TextChannel):
        '''Kies welk kanaal je wilt gebruiken.'''
        self.utils.settings['starboard']['channel'] = channel.id
        self.star_channel = self.utils.settings['starboard']['channel']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        channel = message.channel
        emoji = reaction.emoji
        count = reaction.count
        if emoji == self.emoji and self.star_channel and message.id not in self.starred_messages and channel.id != self.star_channel:
            if count >= self.threshold:
                star_channel = self.bot.get_channel(self.star_channel)
                author = message.author
                avatar = author.avatar_url if author.avatar else author.default_avatar_url
                if message.content:
                    text = message.content
                else:
                    text = None

                if message.attachments:
                    attachment = message.attachments[0]
                else:
                    attachment = None

                if text:
                    embed = discord.Embed(color=discord.Color.blurple())
                    embed.add_field(name='Bericht', value='{}'.format(text))
                else:
                    embed = discord.Embed(color=discord.Color.blurple())

                embed.set_author(name='📌 {0.display_name}#{0.discriminator} in {1.name}'.format(author, channel), icon_url=avatar)
                embed.add_field(name='', value='[Jump!]({})'.format(message.jump_url))


                if attachment:
                    embed.set_image(url=attachment.url)

                embed.set_footer(text='{}'.format(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))

                self.starred_messages.append(message.id)
                self.utils.settings['starboard']['messages'] = self.starred_messages
                self.utils.save_settings()

                await star_channel.send(embed=embed)
