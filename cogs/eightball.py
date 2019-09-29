from discord.ext import commands
from random import choice


class Eightball:
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils
        self.answers = [
            'Het is zeker.',
            'Het is zo besloten.',
            'Zonder enige twijfel.',
            'Je kunt erop vertrouwen.',
            'Volgens mij wel.',
            'Zeer waarschijnlijk.',
            'Goed vooruitzicht.',
            'Vooruitzicht is wazig, probeer het opnieuw.',
            'Vraag later opnieuw.',
            'Dat kan ik je beter niet vertellen.',
            'Momenteel niet te voorspellen.',
            'Concentreer je en vraag opnieuw.',
            'Reken er maar niet op.',
            'Mijn antwoord is nee.',
            'Mijn bronnen zeggen van niet.',
            'Vooruitzicht is niet zo goed.',
            'Zeer twijfelachtig.',
            'Hahahaha! :joy:',
            'Nee, gewoon nee.',
            'Zou je dat wel willen?',
            'Doe ff normaal.',
            'Heb je nou niets beters te melden?',
            'Ja, kek!',
            'Misschien wel.',
            'Vandaag heb je geluk.',
            'God zegent U.',
            'Dat kun je beter aan iemand anders vragen.',
            'Ik zou nu niet in jouw schoenen willen staan.',
            'Het ziet er zeer slecht uit.',
            'Th8 zegt nee.',
        ]

    @commands.command(name='8ball', aliases=['8'])
    async def eightball(self, context):
        '''Voor als je er zelf niet meer uitkomt.'''
        question = context.message.content[4:]
        if not question.endswith('?'):
            question += '?'
        await context.send('_{}_ **{}**'.format(question.capitalize(), choice(self.answers)))
        await context.message.delete()
