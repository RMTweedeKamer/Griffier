class Pinner:
    def __init__(self, bot, utils):
        self.bot = bot
        self.utils = utils
        self.threshold = 4

    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        emoji = reaction.emoji
        count = reaction.count
        if emoji == '📌':
            if count >= self.threshold:
                await message.pin()

    async def on_reaction_remove(self, reaction, user):
        message = reaction.message
        emoji = reaction.emoji
        count = reaction.count
        if emoji == '📌':
            if count < 1:
                await message.unpin()
