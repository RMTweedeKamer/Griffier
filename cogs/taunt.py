import discord
from random import choice
from discord.ext import commands


# TODO

class Taunt():
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils
        self.taunts = [
            ':ship: **LATEN WE INDIE HEROVEREN!** :crossed_swords:',
            'Mods = Gods ...',
            ':clap: RMTK :clap: is :clap: grindr :clap: voor :clap: internetautisten :clap:',
            '**Zet een STREEP! door de democratie!**'
        ]

    @commands.command(name='taunt')
    async def taunt(self, context):
        if self.utils.jail_check(context.command, context.channel.id):
            await context.message.delete()
            await context.send(choice(self.taunts))
