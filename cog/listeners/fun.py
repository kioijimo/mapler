from discord import Embed, RawReactionActionEvent
from discord.ext.commands import Cog

from bot.bot import Mapler
from cog import ABCCog


class FunListener(ABCCog):
    def __init__(self, bot: Mapler):
        super().__init__(bot)

        """
        TODO:

            Add a subscription to the shamed message and update the amount of shames received until 24 hours.
        """

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):

        shame_emojis = [1569608163165216798]
        HALL_OF_SHAME_CHANNEL_ID = 1569594607463960696

        if payload.emoji.id not in shame_emojis:
            return

        guild = self.bot.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        author = message.author

        if author.bot:
            return

        shames = sum(
            [
                r.count
                for r in message.reactions
                if not isinstance(r.emoji, str)
                and r.emoji.id in shame_emojis
                or r.emoji in shame_emojis
            ]
        )

        if shames < 1:
            return

        shame_channel = guild.get_channel(HALL_OF_SHAME_CHANNEL_ID)

        embed = (
            Embed(
                color=self.bot.embed_color,
                title=f"{author.display_name} received {shames} shame{'s' if shames > 2 else ''}",
            )
            .set_author(
                name=author.name,
                icon_url=author.display_avatar.url,
            )
            .add_field(name=" ", value="")
            .add_field(
                name="Content",
                value=f"> {message.content if len(message.content) > 0 else '*No content in the message*'}",
                inline=False,
            )
            .add_field(
                name="Source", value=f"[Jump!]({message.jump_url})", inline=False
            )
            .set_footer(text=f"Sent at {message.created_at.strftime('%b %d, %Y | %r')}")
        )

        if len(message.attachments) > 0:
            embed.set_image(url=message.attachments[0].url)

        await shame_channel.send(embed=embed)


async def setup(bot: Mapler):
    await bot.add_cog(FunListener(bot))
