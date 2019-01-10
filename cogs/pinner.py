class Pinner:
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils
        self.emoji = '📌'

    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        channel = message.channel
        emoji = reaction.emoji

        if emoji == self.emoji:
            pins = await channel.pins()
            if len(pins) >= 50:
                first_pin = pins[-1]
                await first_pin.unpin()
            await message.pin()

    async def on_reaction_remove(self, reaction, user):
        message = reaction.message
        emoji = reaction.emoji
        count = reaction.count
        if emoji == self.emoji and count < 1:
            await message.unpin()
