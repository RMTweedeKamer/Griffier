import asyncio
import praw
import discord
from discord.ext import commands


class Aankondigingen:
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils

        if 'aankondigingen' not in self.utils.settings:
            self.utils.settings['aankondigingen'] = {}
        if 'client_id' not in self.utils.settings['aankondigingen']:
            self.utils.settings['aankondigingen']['client_id'] = None
        if 'client_secret' not in self.utils.settings['aankondigingen']:
            self.utils.settings['aankondigingen']['client_secret'] = None
        if 'mededeling_kanaal' not in self.utils.settings['aankondigingen']:
            self.utils.settings['aankondigingen']['mededeling_kanaal'] = None
        if 'stemmingen_kanaal' not in self.utils.settings['aankondigingen']:
            self.utils.settings['aankondigingen']['stemmingen_kanaal'] = None
        if 'entries' not in self.utils.settings['aankondigingen']:
            self.utils.settings['aankondigingen']['entries'] = []

        self.utils.save_settings()

        self.flairs_normal = {
                        'MOTIE': {'channel': 'mededeling_kanaal', 'color': '50004F'},
                        'WETSVOORSTEL': {'channel': 'mededeling_kanaal', 'color': 'E39088'},
                        'KAMERSTUK': {'channel': 'mededeling_kanaal', 'color': '048ABF'},
                        'META': {'channel': 'mededeling_kanaal', 'color': 'B9005C'},
                        'PARLEMENT': {'channel': 'mededeling_kanaal', 'color': 'D8C50F'},
                        'DEBAT': {'channel': 'mededeling_kanaal', 'color': 'CD392F'}
        }
        self.flairs_stemmingen = {
                        'EK STEMMING': {'channel': 'stemmingen_kanaal', 'color': '7FD47F'},
                        'TK STEMMING': {'channel': 'stemmingen_kanaal', 'color': '7FD47F'}
        }
        self.flairs_resultaten = {
                        'UITSLAGEN': {'channel': 'stemmingen_kanaal', 'color': '6E7B04'}
        }
        self.channels = {
                         'stemmingen_kanaal': self.utils.settings['aankondigingen']['stemmingen_kanaal'],
                         'mededeling_kanaal': self.utils.settings['aankondigingen']['mededeling_kanaal']
                        }

        client_id = 'xBtJB0-uZBsEDQ'
        client_secret = 'gbcQeXIszJFAjjiY3JYP-ptedkQ'

        self.subreddit = 'rmtk'

        self.entries = self.utils.settings['aankondigingen']['entries']

        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  user_agent='Griffier/1.0')

        bot.loop.create_task(self.read_feeds())

    @commands.group(name='aankondiging')
    @commands.is_owner()
    async def aankondiging(self, context):
        '''Instellingen voor aankondigingen'''

    @aankondiging.command(name='stemmingen')
    async def aankondiging_set_stemmingen(self, context, kanaal: discord.TextChannel):
        '''Stel een kanaal in waar de stemmingen moeten worden gedeeld'''
        self.utils.settings['aankondigingen']['stemmingen_kanaal'] = kanaal.id
        self.channels['stemmingen_kanaal'] = self.utils.settings['aankondigingen']['stemmingen_kanaal']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    @aankondiging.command(name='mededelingen')
    async def aankondiging_set_medelingen(self, context, kanaal: discord.TextChannel):
        '''Stel een kanaal in waar de mededelingen moeten worden gedeeld'''
        self.utils.settings['aankondigingen']['mededeling_kanaal'] = kanaal.id
        self.channels['mededeling_kanaal'] = self.utils.settings['aankondigingen']['mededeling_kanaal']
        self.utils.save_settings()
        await context.message.add_reaction('\U0001F44D')

    async def read_feeds(self):
        await asyncio.sleep(10)
        while True:
            if self.channels['stemmingen_kanaal'] and self.channels['mededeling_kanaal']:
                for submission in self.reddit.subreddit(self.subreddit).new(limit=5):
                    if submission.id not in self.entries:
                        if str(submission.link_flair_text) in self.flairs_normal:
                            shortlink = submission.shortlink
                            title = submission.title

                            title = title.split(':')
                            event = self.flairs_normal[str(submission.link_flair_text)]
                            channel = self.bot.get_channel(self.channels[event['channel']])
                            if len(title) > 1:
                                title = '[{}] {}'.format(title[0], title[1])
                            else:
                                title = title[0]
                            embed = discord.Embed(title=title,
                                                  url=shortlink,
                                                  color=discord.Color(int(event['color'], 16)))
                            await channel.send(embed=embed)

                            self.entries.append(submission.id)
                            self.utils.settings['aankondigingen']['entries'] = self.entries
                            self.utils.save_settings()

                            await asyncio.sleep(2)
                        elif str(submission.link_flair_text) in self.flairs_stemmingen:
                            shortlink = submission.shortlink
                            title = submission.title

                            event = self.flairs_stemmingen[str(submission.link_flair_text)]
                            channel = self.bot.get_channel(self.channels[event['channel']])

                            embed = discord.Embed(title=title,
                                                  url=shortlink,
                                                  color=discord.Color(int(event['color'], 16)))

                            await channel.send(embed=embed)

                            self.entries.append(submission.id)
                            self.utils.settings['aankondigingen']['entries'] = self.entries
                            self.utils.save_settings()

                            await asyncio.sleep(2)
                        elif str(submission.link_flair_text) in self.flairs_resultaten:
                            shortlink = submission.shortlink
                            title = submission.title

                            event = self.flairs_resultaten[str(submission.link_flair_text)]
                            channel = self.bot.get_channel(self.channels[event['channel']])

                            embed = discord.Embed(title=title,
                                                  url=shortlink,
                                                  color=discord.Color(int(event['color'], 16)))

                            await channel.send(embed=embed)

                            self.entries.append(submission.id)
                            self.utils.settings['aankondigingen']['entries'] = self.entries
                            self.utils.save_settings()

                            await asyncio.sleep(2)
            await asyncio.sleep(10)
