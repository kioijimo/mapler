from discord.ext.commands import Cog

from bot import Mapler


class ABCCog(Cog):
    def __init__(self, bot: Mapler):
        self.bot = bot
        self.session = bot.session
        self.logger = bot.logger
