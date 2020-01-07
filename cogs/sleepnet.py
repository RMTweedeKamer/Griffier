import discord
from discord.ext import commands
from datetime import datetime
import difflib


class Sleepnet(commands.Cog):
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils

        if 'sleepnet' not in self.utils.settings:
            self.utils.settings['sleepnet'] = {}
        if 'channel' not in self.utils.settings['sleepnet']:
            self.utils.settings['sleepnet']['channel'] = ''

        self.utils.save_settings()

        self._channel = self.utils.settings['sleepnet']['channel']
        self.attachment_path = 'data'

        self.green = discord.Color.green()
        self.orange = discord.Color.orange()
        self.red = discord.Color.red()
        self.blue = discord.Color.blue()
        self.black = discord.Color.from_rgb(15, 2, 2)

    @commands.command(name='sleepnetchannel')
    @commands.is_owner()
    async def set_channel(self, context, channel: discord.TextChannel):
        '''Kies welk kanaal je wilt gebruiken.'''
        self._channel = channel.id
        self.utils.settings['sleepnet']['channel'] = self._channel
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    async def downloadattachment(self, data, url, filename, message_id):

        with open(self.attachment_path+'/{}-{}'.format(message_id, filename), "wb") as f:
            f.write(data)

        return '{}-{}'.format(message_id, filename)

    async def _send_message_to_channel(self, guild, content=None, embed=None, attachment=None):

        channel = discord.utils.get(self.bot.get_all_channels(), id=self._channel)
        # Check if the channel exists at all
        if channel:
            # Check if there's an embed
            if embed:
                await channel.send(content=content, embed=embed)
            # If it's an attachment, send the attachment.
            if attachment:
                await channel.send(content=content, file=discord.File(attachment))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild = message.guild
        author = message.author
        channel = message.channel

        if isinstance(channel, discord.abc.GuildChannel):
            if author.id != self.bot.user.id:

                    embed = discord.Embed(color=self.red)
                    embed.set_thumbnail(url=author.avatar_url)
                    embed.set_author(name='Bericht verwijderd')
                    embed.add_field(name='Gebruiker', value='{0.name}#{0.discriminator}\n({0.id})'.format(author))

                    embed.add_field(name='Kanaal', value=message.channel.mention)
                    if message.content:
                        embed.add_field(name='Bericht', value=message.clean_content, inline=False)

                    embed.set_footer(text='Bericht ID: {} | {}'.format(message.id,
                                                                       datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))

                    await self._send_message_to_channel(guild, embed=embed)

                    if message.attachments:
                        attachment = message.attachments[0]
                        attachement_data = await attachment.read(use_cached=True)
                        filename = await self.downloadattachment(attachement_data,
                                                                 attachment.url,
                                                                 attachment.filename,
                                                                 message.id)
                        message = 'Bijlagen voor bericht: {}'.format(message.id)
                        await self._send_message_to_channel(guild,
                                                            content=message,
                                                            attachment=self.attachment_path+'/'+filename)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        guild = after.guild
        author = after.author
        channel = after.channel

        if isinstance(channel, discord.abc.GuildChannel):

                if author.id != self.bot.user.id and before.clean_content != after.clean_content:

                    embed = discord.Embed(color=self.blue)
                    embed.set_thumbnail(url=author.avatar_url)
                    embed.set_author(name='Bericht aangepast')
                    embed.add_field(name='Gebruiker', value='{0.name}#{0.discriminator}\n({0.id})'.format(author))
                    embed.add_field(name='Kanaal', value=before.channel.mention)
                    embed.add_field(name='Voor aanpassing', value=before.clean_content, inline=False)
                    embed.add_field(name='Na aanpassing', value=after.clean_content, inline=False)
                    embed.add_field(name='Link', value='[Ga naar dit bericht]({})'.format(after.jump_url), inline=False)
                    embed.set_footer(text='Bericht ID: {} | {}'.format(after.id,
                                                                       datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))

                    await self._send_message_to_channel(guild, embed=embed)
