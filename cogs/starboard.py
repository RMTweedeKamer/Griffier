import discord
from discord.ext import commands
from datetime import datetime


class Starboard(commands.Cog):
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils

        if 'starboard' not in self.utils.settings:
            self.utils.settings['starboard'] = {}
        if 'messages' not in self.utils.settings['starboard']:
            self.utils.settings['starboard']['messages'] = {}
        if 'channel' not in self.utils.settings['starboard']:
            self.utils.settings['starboard']['channel'] = None
        if 'threshold' not in self.utils.settings['starboard']:
            self.utils.settings['starboard']['threshold'] = 4

        self.utils.save_settings()

        self.star_channel = self.utils.settings['starboard']['channel']
        self.threshold = self.utils.settings['starboard']['threshold']
        self.starred_messages = self.utils.settings['starboard']['messages']

        self.emoji = '⭐'




    @commands.group(name='starboard')
    @commands.is_owner()
    @commands.has_role(488363614294507541)
    async def starboard(self, context):
        '''Instellingen voor starboard'''
        if self.utils.jail_check(context.command, context.channel.id):
            if not context.invoked_subcommand:
                await self.utils.send_cmd_help(context)

    @starboard.command(name='threshold')
    async def set_threshold(self, context, threshold: int):
        '''threshold'''
        self.utils.settings['starboard']['threshold'] = threshold
        self.threshold = self.utils.settings['starboard']['threshold']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    @starboard.command(name='channel')
    async def set_channel(self, context, channel: discord.TextChannel):
        '''Kies welk kanaal je wilt gebruiken.'''
        self.utils.settings['starboard']['channel'] = channel.id
        self.star_channel = self.utils.settings['starboard']['channel']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        channel = message.channel
        emoji = reaction.emoji
        count = reaction.count
        if emoji == self.emoji and str(message.id) not in self.starred_messages and self.star_channel and channel.id != self.star_channel:
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

                    embed.add_field(name='Link', value='[Ga naar dit bericht]({})'.format(message.jump_url),  inline=False)
                    embed.set_author(name='📌 {0.display_name}#{0.discriminator} in #{1.name}'.format(author, channel), icon_url=avatar)

                    if attachment:
                        embed.set_image(url=attachment.url)

                    embed.set_footer(text='{}'.format(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))



                    starboard_message = await star_channel.send(embed=embed)

                    self.starred_messages[str(message.id)] = starboard_message.id

                    self.utils.settings['starboard']['messages'] = self.starred_messages

                    self.utils.save_settings()

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        message = reaction.message
        channel = message.channel
        emoji = reaction.emoji
        count = reaction.count
        if emoji == self.emoji and str(message.id) in self.starred_messages and self.star_channel and channel.id != self.star_channel:
                if count < self.threshold:
                    star_channel = self.bot.get_channel(self.star_channel)
                    starred_message = await star_channel.fetch_message(self.starred_messages[str(message.id)])
                    await starred_message.delete()

                    del self.starred_messages[str(message.id)]
                    self.utils.settings['starboard']['messages'] = self.starred_messages
                    self.utils.save_settings()
