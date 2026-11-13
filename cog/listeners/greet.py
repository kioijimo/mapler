import json

from discord import Embed, Member, TextChannel
from discord.ext.commands import Cog
from sqlmodel import select

from main import Mapler
from service.db import models

from .. import ABCCog


class GreetingListener(ABCCog, name="Greeting Event"):
    """
    Everything greeting-related events of me! From welcome messages, automatic member update on join and leave, and more!
    """

    def __init__(self, bot: Mapler):
        super().__init__(bot)
        self.new_members = []

    @Cog.listener()
    async def on_member_join(self, member: Member):
        guild = self.session.get(models.Guild, member.guild.id)

        cog = self.session.exec(
            select(models.Cog).where(models.Cog.name == "Greeting")
        ).one()

        action = self.session.exec(
            select(models.Action).where(
                models.Action.name == "welcome" and models.Action.cog_id == cog.id
            )
        ).one()

        greeting = self.session.exec(
            select(models.ActionGreeting).where(
                models.ActionGreeting.action_id == action.id,
                models.ActionGreeting.guild_id == guild.id,
            )
        ).one_or_none()

        if not greeting:
            return

        if greeting.welcome_trig.split("|")[0] != "on_member_join":
            self.new_members.append(member)
            return

        msg = greeting.welcome_msg.replace("{member.mention}", member.mention)
        embed = (
            self.json_to_embed(
                greeting.welcome_embed.replace("{member.mention}", member.mention)
            )
            if greeting.welcome_embed is not None
            else None
        )
        ch = member.guild.get_channel(greeting.welcome_ch)

        await ch.send(msg, embed=embed)

    @Cog.listener()
    async def on_member_update(self, _, member: Member):
        guild = self.session.get(models.Guild, member.guild.id)

        cog = self.session.exec(
            select(models.Cog).where(models.Cog.name == "Greeting")
        ).one()

        action = self.session.exec(
            select(models.Action).where(
                models.Action.name == "welcome" and models.Action.cog_id == cog.id
            )
        ).one()

        greeting = self.session.exec(
            select(models.ActionGreeting).where(
                models.ActionGreeting.action_id == action.id,
                models.ActionGreeting.guild_id == guild.id,
            )
        ).one_or_none()

        if not greeting:
            return

        trig_split = greeting.welcome_trig.split("|")
        trigger = trig_split[0]
        trig_role = int(trig_split[1])

        if trigger != "on_member_update":
            return

        found = next(
            filter(
                lambda m: (
                    m.id == member.id
                    and next(
                        filter(
                            lambda role: role.id == trig_role,
                            reversed(member.roles),
                        ),
                        False,
                    )
                ),
                self.new_members,
            ),
            False,
        )

        if not found:
            return

        self.new_members.remove(member)

        ch = member.guild.get_channel(greeting.welcome_ch)
        if isinstance(ch, TextChannel):
            msg = greeting.welcome_msg.replace("{member.mention}", member.mention)
            embed = (
                self.json_to_embed(
                    greeting.welcome_embed.replace("{member.mention}", member.mention)
                )
                if greeting.welcome_embed is not None
                else None
            )

            await ch.send(msg, embed=embed)

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        channel = self.bot.get_channel(1563706475833204827)

        if isinstance(channel, TextChannel):
            await channel.send(f"Wow umalis. Kapal ng mukha {member.mention}!!")

    def json_to_embed(self, string: str):
        """Convert a json string to a discord embed
        Args:
            string (str): JSON string
        Returns:
            discord.Embed: Resulting embed
        """
        data = json.loads(string)

        embed = Embed()
        empty = None

        for field in ("title", "description", "color", "url"):
            if field in data and data[field] != "" and data[field] is not None:
                setattr(embed, field, data[field])
            else:
                setattr(embed, field, empty)

        if "author" in data:
            if (
                "name" in data["author"]
                and data["author"]["name"] != ""
                and data["author"]["name"] is not None
            ):
                name = data["author"]["name"]
            else:
                name = empty

            if (
                "url" in data["author"]
                and data["author"]["url"] != ""
                and data["author"]["url"] is not None
            ):
                url = data["author"]["url"]
            else:
                url = empty

            if (
                "icon" in data["author"]
                and data["author"]["icon"] != ""
                and data["author"]["icon"] is not None
            ):
                icon = data["author"]["icon"]
            else:
                icon = empty

            if name != empty or url != empty or icon != empty:
                embed.set_author(name=name, url=url, icon_url=icon)

        if (
            "thumbnail" in data
            and data["thumbnail"] != ""
            and data["thumbnail"] is not None
        ):
            embed.set_thumbnail(url=data["thumbnail"])

        if "fields" in data:
            for field in data["fields"]:
                if "inline" not in field or field["inline"]:
                    inline = True
                else:
                    inline = False

                if (
                    "name" in field
                    and field["name"] != ""
                    and field["name"] is not None
                ):
                    name = field["name"]
                else:
                    name = empty

                if (
                    "value" in field
                    and field["value"] != ""
                    and field["value"] is not None
                ):
                    value = field["value"]
                else:
                    value = empty

                embed.add_field(name=name, value=value, inline=inline)

        if "footer" in data and data["footer"] != {} and data["footer"] is not None:
            if (
                "text" in data["footer"]
                and data["footer"]["text"] != ""
                and data["footer"]["text"] is not None
            ):
                text = data["footer"]["text"]
            else:
                text = empty

            if (
                "icon_url" in data["footer"]
                and data["footer"]["icon_url"] != ""
                and data["footer"]["icon_url"] is not None
            ):
                icon_url = data["footer"]["icon_url"]
            else:
                icon_url = empty

            if icon_url != empty or text != empty:
                embed.set_footer(text=text, icon_url=icon_url)

        return embed


async def setup(bot: Mapler):
    await bot.add_cog(GreetingListener(bot))
