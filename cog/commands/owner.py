from discord.ext.commands import Context, hybrid_command, is_owner

from main import Mapler

from .. import ABCCog


class Owner(ABCCog):
    def __init__(self, bot: Mapler):
        super().__init__(bot)

    @hybrid_command(name="sync", description="Sync my commands")
    @is_owner()
    async def sync(self, ctx: Context):
        synced = await self.bot.tree.sync()

        await ctx.reply(f"Synced {len(synced)} commands!", ephemeral=True)

    @hybrid_command(name="purge", description="Purge every message in a channel")
    @is_owner()
    async def purge(self, ctx: Context):
        await ctx.defer(ephemeral=True)
        await ctx.channel.purge(limit=999999999999999999)

        await ctx.reply("Deleted every message here!", ephemeral=True)


async def setup(bot: Mapler):
    await bot.add_cog(Owner(bot))
