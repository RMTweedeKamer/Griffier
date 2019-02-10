import asyncio
import praw
import discord
from discord.ext import commands


class Flair:
    def __init__(self, flair_type, channel, color):
        self.type = flair_type
        self.channel = channel
        self.color = color

    def color_int(self):
        return int(self.color, 16)


class Announcements:
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils

        if 'announcements' not in self.utils.settings:
            self.utils.settings['announcements'] = {}
        if 'client_id' not in self.utils.settings['announcements']:
            self.utils.settings['announcements']['client_id'] = None
        if 'client_secret' not in self.utils.settings['announcements']:
            self.utils.settings['announcements']['client_secret'] = None
        if 'announcement_channel' not in self.utils.settings['announcements']:
            self.utils.settings['announcements']['announcement_channel'] = None
        if 'vote_channel' not in self.utils.settings['announcements']:
            self.utils.settings['announcements']['vote_channel'] = None
        if 'media_channel' not in self.utils.settings['announcements']:
            self.utils.settings['announcements']['media_channel'] = None
        if 'entries' not in self.utils.settings['announcements']:
            self.utils.settings['announcements']['entries'] = []

        self.utils.save_settings()

        self.flairs = {
                    'MOTIE':        Flair(flair_type='normal',  channel='announcement_channel', color='50004F'),
                    'WETSVOORSTEL': Flair(flair_type='normal',  channel='announcement_channel', color='E39088'),
                    'KAMERSTUK':    Flair(flair_type='normal',  channel='announcement_channel', color='048ABF'),
                    'META':         Flair(flair_type='normal',  channel='announcement_channel', color='B9005C'),
                    'PARLEMENT':    Flair(flair_type='normal',  channel='announcement_channel', color='D8C50F'),
                    'DEBAT':        Flair(flair_type='normal',  channel='announcement_channel', color='CD392F'),
                    'EK STEMMING':  Flair(flair_type='votingek',  channel='vote_channel', color='7FD47F'),
                    'TK STEMMING':  Flair(flair_type='votingtk',  channel='vote_channel', color='7FD47F'),
                    'UITSLAGEN':    Flair(flair_type='results', channel='vote_channel', color='6E7B04'),
                    'VRAGENUUR':    Flair(flair_type='questions', channel='announcement_channel', color='ADD4D6')
                    }

        self.channels = {
                         'vote_channel': self.utils.settings['announcements']['vote_channel'],
                         'announcement_channel': self.utils.settings['announcements']['announcement_channel'],
                         'media_channel': self.utils.settings['announcements']['media_channel']
                        }

        client_id = 'xBtJB0-uZBsEDQ'
        client_secret = 'gbcQeXIszJFAjjiY3JYP-ptedkQ'

        self.subreddit = 'rmtk'
        self.media_subreddit = 'rmtkmedia'

        self.entries = self.utils.settings['announcements']['entries']

        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  user_agent='Griffier/1.0')

        bot.loop.create_task(self.read_feeds())

    @commands.command(name='remind', aliases=['remindme'])
    async def set_reminder_role(self, context):
        '''Toggle the Reminders role of the user'''
        role = discord.utils.get(context.guild.roles, name="Reminders")
        if role in context.author.roles:
            await context.author.remove_roles(role)
        else:
            await context.author.add_roles(role)

    @commands.group(name='announcement')
    @commands.has_any_role('Secretaris-Generaal', 'Developer')
    async def announcement(self, context):
        '''Instellingen voor aankondigingen'''
        if not context.invoked_subcommand:
            await self.utils.send_cmd_help(context)

    @announcement.command(name='vote', aliases=['stemmingen'])
    async def set_vote_announcement(self, context, channel: discord.TextChannel):
        '''Stel een kanaal in waar de stemmingen moeten worden gedeeld'''
        self.utils.settings['announcements']['vote_channel'] = channel.id
        self.channels['vote_channel'] = self.utils.settings['announcements']['vote_channel']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    @announcement.command(name='announcements', aliases=['mededelingen'])
    async def set_announcement(self, context, channel: discord.TextChannel):
        '''Stel een kanaal in waar de mededelingen moeten worden gedeeld'''
        self.utils.settings['announcements']['announcement_channel'] = channel.id
        self.channels['announcement_channel'] = self.utils.settings['announcements']['announcement_channel']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    @announcement.command(name='media')
    async def set_media_announcement(self, context, channel: discord.TextChannel):
        '''Stel een kanaal in waar de media berichten moet worden gedeeld'''
        self.utils.settings['announcements']['media_channel'] = channel.id
        self.channels['media_channel'] = self.utils.settings['announcements']['media_channel']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    @announcement.command(name='force')
    @commands.has_any_role('Developer')
    async def force_update(self, context):
        '''Send announcements for the last submissions posted to the appropriate channels'''
        for submission in self.reddit.subreddit(self.media_subreddit).new(limit=5):
            if self.channels['media_channel']:
                await self.send_announcement(submission, media_submission=True)
        for submission in self.reddit.subreddit(self.subreddit).new(limit=5):
            if self.channels['vote_channel'] and self.channels['announcement_channel']:
                await self.send_announcement(submission)
        await context.message.add_reaction('\U0001F44D')

    async def read_feeds(self):
        await asyncio.sleep(10)
        while True:
            try:
                if self.channels['media_channel']:
                    for submission in self.reddit.subreddit(self.media_subreddit).new(limit=5):
                        if submission.id not in self.entries:
                            await self.send_announcement(submission, media_submission=True)
                if self.channels['vote_channel'] and self.channels['announcement_channel']:
                    for submission in self.reddit.subreddit(self.subreddit).new(limit=5):
                        if submission.id not in self.entries:
                            await self.send_announcement(submission)
            except Exception:
                pass
            await asyncio.sleep(10)

    async def send_announcement(self, submission, media_submission=False):
        shortlink = submission.shortlink
        title = submission.title

        if media_submission:
            if submission.link_flair_text:
                title = '[{}] {}'.format(submission.link_flair_text, submission.title)
            channel = self.bot.get_channel(self.channels['media_channel'])
            color = int('6E7B04', 16)
        else:
            flair = self.flairs[str(submission.link_flair_text)]
            color = flair.color_int()
            channel = self.bot.get_channel(self.channels[flair.channel])
            if flair.type == 'normal' and ':' in title:
                title = title.split(':')
                title = '[{}] {}'.format(title[0], title[1])
            elif flair.type == 'votingek':
                role = discord.utils.get(channel.guild.roles, name='Eerste Kamerlid')
            elif flair.type == 'votingtk':
                role = discord.utils.get(channel.guild.roles, name='Tweede Kamerlid')
            else:
                role = discord.utils.get(channel.guild.roles, name='Reminders')
            await channel.send(role.mention())

        embed = discord.Embed(title=title,
                              url=shortlink,
                              color=discord.Color(color))
        await channel.send(embed=embed)

        self.entries.append(submission.id)
        self.utils.settings['announcements']['entries'] = self.entries
        self.utils.save_settings()

        await asyncio.sleep(2)

