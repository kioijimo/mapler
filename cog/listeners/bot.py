from discord import Guild
from discord.ext.commands import Cog

from bot.bot import Mapler
from cog import ABCCog
from service.db import models


class BotListener(ABCCog):
    def __init__(self, bot: Mapler):
        super().__init__(bot)

    @Cog.listener()
    async def on_guild_join(self, guild: Guild):
        self.session.add(models.Guild(id=guild.id, name=guild.name))
        self.session.commit()

    @Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        self.session.delete(self.session.get(models.Guild, guild.id))
        self.session.commit()

    @Cog.listener()
    async def on_guild_update(self, before: Guild, after: Guild):
        guild = self.session.get(models.Guild, before.id)

        if not guild:
            return

        if guild.name == after.name:
            return

        guild.name = after.name

        self.session.add(guild)
        self.session.commit()


async def setup(bot: Mapler):
    await bot.add_cog(BotListener(bot))
