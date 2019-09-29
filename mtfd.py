from discord.ext import commands
from random import choice


class Eightball:
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils
        self.answers = [
            'Het is een links complot.',
            'Het is de schuld van de mods.',
        ]

    # @commands.command(name='mtfd', aliases=['mtfd'])
    # async def mtfd(self, context):
    #     '''Voor als je er zelf niet meer uitkomt.'''
    #     question = context.message.content[4:]
    #     if not question.endswith('?'):
    #         question += '?'
    #     await context.send('_{}_ **{}**'.format(question.capitalize(), choice(self.answers)))
