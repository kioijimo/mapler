from discord import CategoryChannel, ForumChannel
from discord.abc import GuildChannel
from discord.ext.commands import (
    Bot,
    Context,
    hybrid_command,
)
from discord.ext.commands.cooldowns import PrivateChannel

from main import Mapler

from .. import ABCCog


class Utils(ABCCog, name="Utility"):
    """
    Every command for utility-use!
    """

    def __init__(self, bot: Mapler):
        super().__init__(bot)

    @hybrid_command(name="ping", description="Ping me and retrieve my latency")
    async def ping(self, ctx: Context):
        await ctx.send(f"Pong! My latency is {round(self.bot.latency * 1000)}ms.")

    @hybrid_command(name="say", description="Relay a message through me")
    async def say(
        self, ctx: Context[Bot], message: str, channel: GuildChannel | None = None
    ):
        await ctx.defer()
        ch = ctx.bot.get_channel(channel.id if channel != None else ctx.channel.id)

        if ch != None and not isinstance(
            ch, (PrivateChannel, CategoryChannel, ForumChannel)
        ):
            await ch.send(message)

        if ctx.interaction:
            await ctx.reply("Relayed your message!", ephemeral=True, delete_after=3)
        else:
            await ctx.message.delete()


async def setup(bot: Mapler):
    await bot.add_cog(Utils(bot))
