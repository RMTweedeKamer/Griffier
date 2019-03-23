import discord
from discord.ext import commands


# TODO

class Taunt():
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils
        self.taunts = [
            ':ship: **LATEN WE INDIE HEROVEREN!** :crossed_swords:',
            'haha sp dom',
            'Hielke is 7.',
            'Mods = Gods ...',
            ':clap: RMTK :clap: is :clap: grindr :clap: voor :clap: internetautisten :clap:',
            '**Zet een STREEP! door de democratie!**'
        ]

    @commands.command(name='taunt')
    async def taunt(self, context, *, taunt: str):
        await context.message.delete()

        try:
          await context.send(self.taunts[int(taunt)])
        except:
          pass
